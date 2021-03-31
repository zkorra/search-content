import { Component, OnInit, Input } from '@angular/core';
import {
  Validators,
  FormControl,
  FormGroup,
  FormBuilder,
} from '@angular/forms';
import { ContentState } from '../../search/search.state';
import { SearchContent, GetEngines } from '../../search/search.action';
import { Select, Store } from '@ngxs/store';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
  providers: [MessageService],
})
export class HomePageComponent implements OnInit {
  @Select(ContentState.getContentList)
  contents: any;

  @Select(ContentState.getEngineList)
  engines: any;

  searchForm!: FormGroup;

  searchedParams: any;

  engineList = [];

  contentList = [];

  allColumns: any[] = [];

  selectedContentList: any[] = [];

  warpSelectedColumns: any[] = [];

  selectedExampleRow: any = {};

  isDisplayDialog = false;

  types = [
    { key: 'Article', value: 'article' },
    { key: 'Course', value: 'course' },
  ];

  regions = [
    { key: 'All', value: '' },
    { key: 'Thailand', value: 'countryTH' },
    { key: 'United States', value: 'countryUS' },
  ];

  constructor(
    private store: Store,
    private fb: FormBuilder,
    private messageService: MessageService
  ) {}

  async ngOnInit(): Promise<void> {
    this.fetchEngines();

    this.searchForm = this.fb.group({
      contentType: new FormControl('', Validators.required),
      searchEngineId: new FormControl('', Validators.required),
      keyword: new FormControl('', Validators.required),
      page: new FormControl(''),
      region: new FormControl(''),
    });
  }

  async fetchEngines(): Promise<void> {
    await this.store.dispatch(new GetEngines()).toPromise();

    await this.engines.subscribe((data: any) => {
      if (data) {
        this.engineList = data;
      }
    });
  }

  async searchContent(params: any): Promise<void> {
    await this.store
      .dispatch(new SearchContent(params))
      .pipe(
        catchError(async (error) =>
          this.messageService.add({
            severity: 'error',
            summary: `${error.status} - ${error.error.error}`,
            detail: `${error.error.message}`,
          })
        )
      )
      .toPromise();

    await this.contents.subscribe((data: any) => {
      if (data) {
        this.contentList = data;
      }
    });
  }

  async onSubmit(value: any): Promise<void> {
    this.selectedContentList = [];

    this.searchForm.controls.contentType.markAsDirty();
    this.searchForm.controls.searchEngineId.markAsDirty();
    this.searchForm.controls.keyword.markAsDirty();

    if (this.searchForm.valid) {
      const {
        contentType,
        searchEngineId,
        keyword,
        page,
        region,
      } = this.searchForm.value;

      this.searchedParams = this.searchForm.value;

      const searchParams: any = {
        type: contentType,
        cx: searchEngineId,
        query: keyword,
        page,
        region,
      };

      this.removeEmptyProperty(searchParams);

      await this.searchContent(searchParams);

      const uniqueKeys = this.filterUniqueKey(this.contentList);

      console.log(this.allColumns);

      const warpColumns: any[] = [];

      uniqueKeys.forEach((key: any) => {
        warpColumns.push({
          field: key,
          header: key[0].toUpperCase() + key.slice(1),
        });
      });

      this.allColumns = warpColumns;
      this.warpSelectedColumns = this.allColumns;
    }
  }

  displayDialog(rowData: any): void {
    this.isDisplayDialog = true;
    this.selectedExampleRow = rowData;
  }

  removeEmptyProperty(object: any): any {
    return Object.keys(object).forEach(
      (key) =>
        (object[key] === undefined || object[key] === '') && delete object[key]
    );
  }

  filterUniqueKey(arrayObject: any[]): any {
    return [
      ...arrayObject.reduce(
        (set, object) => (
          Object.keys(object).forEach((key) => set.add(key)), set
        ),
        new Set()
      ),
    ];
  }

  onEngineChange(event: any): void {
    const { originalEvent, value } = event;

    // mouse event
    if (originalEvent.detail === 1) {
      const selectedEngine: any = this.engineList.find(
        (engine: any) => engine.searchEngineId === value
      );

      this.searchForm.value.contentType = selectedEngine.contentType;
    }
  }

  @Input() get selectedColumns(): any[] {
    return this.warpSelectedColumns;
  }

  set selectedColumns(value: any[]) {
    // restore original order
    this.warpSelectedColumns = this.allColumns.filter((column: any) =>
      value.includes(column)
    );
  }

  goToExternalWebsite(url: string): void {
    window.open(url, '_blank');
  }
}
