import { Component, OnInit } from '@angular/core';
import {
  Validators,
  FormControl,
  FormGroup,
  FormBuilder,
} from '@angular/forms';
import { EngineState } from '../../../engine/engine.state';
import {
  GetEngines,
  CreateEngine,
  UpdateEngine,
  DeleteEngine,
} from '../../../engine/engine.action';
import { Select, Store } from '@ngxs/store';
import { catchError, map } from 'rxjs/operators';
import { ConfirmationService, MessageService } from 'primeng/api';

@Component({
  selector: 'app-engine-table',
  templateUrl: './engine-table.component.html',
  styleUrls: ['./engine-table.component.scss'],
  providers: [MessageService, ConfirmationService],
})
export class EngineTableComponent implements OnInit {
  @Select(EngineState.getEngineList)
  engines: any;

  engineList: any = [];

  engineForm!: FormGroup;

  engineId: any;

  isOpenDialog = false;

  isCreateMode = false;

  types = [
    { key: 'Article', value: 'article' },
    { key: 'Course', value: 'course' },
  ];

  constructor(
    private store: Store,
    private fb: FormBuilder,
    private messageService: MessageService,
    private confirmationService: ConfirmationService
  ) {}

  async ngOnInit(): Promise<void> {
    await this.subscribeEngines();

    this.engineForm = this.fb.group({
      searchEngineId: new FormControl('', Validators.required),
      name: new FormControl('', Validators.required),
      contentType: new FormControl('', Validators.required),
    });
  }

  async subscribeEngines(): Promise<void> {
    await this.engines.subscribe((data: any) => {
      if (data) {
        this.engineList = data;
      }
    });
  }

  async createEngineMode(): Promise<void> {
    this.engineForm.reset();
    this.isCreateMode = true;
    this.isOpenDialog = true;
  }

  async editEngineMode(engineData: any): Promise<void> {
    const engine = await { ...engineData };
    this.engineId = await engine.id;
    this.engineForm.patchValue(engine);
    this.isCreateMode = false;
    this.isOpenDialog = true;
  }

  async saveEngine(): Promise<void> {
    if (this.engineForm.valid) {
      this.isCreateMode
        ? await this.store
            .dispatch(new CreateEngine(this.engineForm.value))
            .pipe(
              map(async (res) => {
                await this.subscribeEngines();
              }),
              catchError(async (error) =>
                this.messageService.add({
                  severity: 'error',
                  summary: `${error.status} - ${error.error.error}`,
                  detail: `${error.error.message}`,
                })
              )
            )
            .toPromise()
        : await this.store
            .dispatch(new UpdateEngine(this.engineId, this.engineForm.value))
            .pipe(
              map(async (res) => {
                await this.subscribeEngines();
              }),
              catchError(async (error) =>
                this.messageService.add({
                  severity: 'error',
                  summary: `${error.status} - ${error.error.error}`,
                  detail: `${error.error.message}`,
                })
              )
            )
            .toPromise();
      this.closeDialog();
    }
  }

  async deleteEngine(engineData: any): Promise<void> {
    this.confirmationService.confirm({
      message: 'Are you sure you want to delete "' + engineData.name + '" ?',
      header: 'Confirm',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        await this.store
          .dispatch(new DeleteEngine(engineData.id))
          .pipe(
            map((res) => {
              this.messageService.add({
                severity: 'success',
                summary: 'Successful',
                detail: 'Engine Deleted',
                life: 3000,
              });
            }),
            catchError(async (error) =>
              this.messageService.add({
                severity: 'error',
                summary: `${error.status}`,
                detail: `${error.error.message}`,
              })
            )
          )
          .toPromise();
      },
    });
  }

  closeDialog(): void {
    this.isOpenDialog = false;
    this.engineForm.reset();
  }
}
