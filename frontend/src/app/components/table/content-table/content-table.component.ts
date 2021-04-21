import { Component, OnInit, Input } from '@angular/core';
import { SearchState } from '../../../search/search.state';
import { SearchContent, GetContentFile } from '../../../search/search.action';
import { Actions, ofActionSuccessful, Select, Store } from '@ngxs/store';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import * as FileSaver from 'file-saver';

@Component({
  selector: 'app-content-table',
  templateUrl: './content-table.component.html',
  styleUrls: ['./content-table.component.scss'],
  providers: [MessageService],
})
export class ContentTableComponent implements OnInit {
  @Select(SearchState.getContentList)
  contents: any;

  @Select(SearchState.getSearchParamss)
  params: any;

  searchParams: any;

  contentList: any = [];

  allColumns: any[] = [];

  selectedContentList: any[] = [];

  warpSelectedColumns: any[] = [];

  selectedExampleRow: any = {};

  isExampleCardDialogOpen = false;

  uniqueColumnsName: any;

  constructor(
    private actions$: Actions,
    private route: ActivatedRoute,
    private store: Store,
    private messageService: MessageService
  ) {
    route.params.subscribe(() => {
      this.fetchContent();
    });
  }

  async ngOnInit(): Promise<void> {
    this.actions$
      .pipe(ofActionSuccessful(SearchContent))
      .subscribe(async () => {
        await this.fetchContent();
      });
  }

  async fetchContent(): Promise<void> {
    await this.params.subscribe((data: any) => {
      if (data) {
        this.searchParams = data;
      }
    });

    this.selectedContentList = [];

    await this.contents.subscribe((data: any) => {
      if (data) {
        this.contentList = data;

        this.uniqueColumnsName = this.filterUniqueKey(this.contentList);

        this.allColumns = this.appendColumnHeader(this.uniqueColumnsName);

        this.warpSelectedColumns = this.allColumns;
      }
    });
  }

  displayExampleCardDialog(rowData: any): void {
    this.isExampleCardDialogOpen = true;
    this.selectedExampleRow = rowData;
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

  appendColumnHeader(columns: any): any {
    const columnsWithHeader: any[] = [];

    columns.forEach((key: any) => {
      columnsWithHeader.push({
        field: key,
        header: key[0].toUpperCase() + key.slice(1),
      });
    });

    return columnsWithHeader;
  }

  appendKeywordColumn(columns?: string[]): any {
    columns?.unshift('keyword');
    return columns;
  }

  appendKeywordProperty(rows: object[]): any {
    return rows.map((element) => ({
      keyword: this.searchParams?.keyword,
      ...element,
    }));
  }

  private saveAsFile(buffer: any, fileName: string, fileType: string): void {
    const data: Blob = new Blob(['\uFEFF' + buffer], { type: fileType });
    FileSaver.saveAs(data, fileName);
  }

  public exportToCsv(
    rows: object[],
    fileName: string,
    columns?: string[]
  ): any {
    if (!rows || !rows.length) {
      return;
    }

    rows = this.appendKeywordProperty(rows);
    columns = this.appendKeywordColumn(columns);

    const separator = ',';
    const keys = Object.keys(rows[0]).filter((k) => {
      if (columns?.length) {
        return columns.includes(k);
      } else {
        return true;
      }
    });

    const csvContent =
      keys.join(separator) +
      '\n' +
      rows
        .map((row: any) => {
          return keys
            .map((k) => {
              let cell = row[k] === null || row[k] === undefined ? '' : row[k];
              cell =
                cell instanceof Date
                  ? cell.toLocaleString()
                  : cell.toString().replace(/"/g, '""');
              if (cell.search(/("|,|\n)/g) >= 0) {
                cell = `"${cell}"`;
              }
              return cell;
            })
            .join(separator);
        })
        .join('\n');
    this.saveAsFile(csvContent, `${fileName}.csv`, 'text/csv;charset=utf-8');
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
