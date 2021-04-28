import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { SearchState } from '../../../search/search.state';
import {
  GetHistory,
  GetContentFile,
  DeleteHistory,
  SetSearchParams,
} from '../../../search/search.action';
import { Select, Store } from '@ngxs/store';
import { ConfirmationService, MessageService } from 'primeng/api';
import { catchError, map } from 'rxjs/operators';

@Component({
  selector: 'app-history-table',
  templateUrl: './history-table.component.html',
  styleUrls: ['./history-table.component.scss'],
  providers: [MessageService, ConfirmationService],
})
export class HistoryTableComponent implements OnInit {
  @Select(SearchState.getHistoryList)
  history: any;

  historyList: any = [];

  regionDict: any = {
    '': 'All',
    countryTH: 'Thailand',
    countryUS: 'United States',
  };

  constructor(
    private store: Store,
    private router: Router,
    private messageService: MessageService,
    private confirmationService: ConfirmationService
  ) {}

  async ngOnInit(): Promise<void> {
    this.fetchHistory();
  }

  async fetchHistory(): Promise<void> {
    await this.store.dispatch(new GetHistory()).toPromise();

    await this.history.subscribe((data: any) => {
      if (data) {
        this.historyList = data;
      }
    });
  }

  async loadContentFile(historyData: any): Promise<void> {
    const {
      keyword,
      contentType,
      page,
      region,
      searchEngineId,
      filename,
    } = historyData;
    const params = {
      keyword,
      contentType,
      page,
      region,
      searchEngineId,
    };

    const filenameEncoded = encodeURIComponent(filename);

    await this.store
      .dispatch(new GetContentFile(filenameEncoded))
      .pipe(
        map(async (res) => {
          await this.store.dispatch(new SetSearchParams(params)).toPromise();
        }),
        catchError(async (error) =>
          this.messageService.add({
            severity: 'error',
            summary: `${error.error.code} - ${error.error.service}`,
            detail: `${error.error.message}`,
          })
        )
      )
      .toPromise();
    this.router.navigate(['/home']);
  }

  async deleteHistory(historyData: any): Promise<void> {
    this.confirmationService.confirm({
      message:
        'Are you sure you want to delete "' +
        historyData.keyword +
        ' ' +
        historyData.contentType +
        '" ?',
      header: 'Confirm',
      icon: 'pi pi-exclamation-triangle',
      accept: async () => {
        await this.store
          .dispatch(new DeleteHistory(historyData.id))
          .pipe(
            map((res) => {
              this.messageService.add({
                severity: 'success',
                summary: 'Successful',
                detail: 'History Deleted',
                life: 3000,
              });
            }),
            catchError(async (error) =>
              this.messageService.add({
                severity: 'error',
                summary: `${error.error.code} - ${error.error.service}`,
                detail: `${error.error.message}`,
              })
            )
          )
          .toPromise();
      },
    });
  }
}
