import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import {
  SearchContent,
  SetSearchParams,
  GetHistory,
  GetContentFile,
  DeleteHistory,
  CheckHistory,
  SaveSelectedContent,
} from './search.action';
import { SearchService } from './search.service';
import { tap } from 'rxjs/operators';

export class SearchStateModel {
  contents: any;
  params: any;
  history: any;
  selectedHistory: any;
}

@Injectable()
@State<SearchStateModel>({
  name: 'search',
  defaults: {
    contents: null,
    params: null,
    history: null,
    selectedHistory: null,
  },
})
export class SearchState {
  constructor(private searchService: SearchService) {}

  @Selector()
  static getContentList(state: SearchStateModel): any {
    return state.contents;
  }

  @Selector()
  static getSearchParamss(state: SearchStateModel): any {
    return state.params;
  }

  @Selector()
  static getHistoryList(state: SearchStateModel): any {
    return state.history;
  }

  @Selector()
  static getSelectedHistory(state: SearchStateModel): any {
    return state.selectedHistory;
  }

  @Action(SearchContent)
  searchContent(
    { getState, setState }: StateContext<SearchStateModel>,
    { searchParams }: SearchContent
  ): any {
    return this.searchService.fetchCustomSearch(searchParams).pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          contents: result,
        });
      })
    );
  }

  @Action(SetSearchParams)
  setSelectedCategory(
    { getState, setState }: StateContext<SearchStateModel>,
    { searchParams }: SetSearchParams
  ): any {
    const state = getState();
    setState({
      ...state,
      params: searchParams,
    });
  }

  @Action(GetHistory)
  getHistory({ getState, setState }: StateContext<SearchStateModel>): any {
    return this.searchService.fetchHistory().pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          history: result,
        });
      })
    );
  }

  @Action(GetContentFile)
  getContentFile(
    { getState, setState }: StateContext<SearchStateModel>,
    { filename }: GetContentFile
  ): any {
    return this.searchService.loadContentFile(filename).pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          contents: result,
        });
      })
    );
  }

  @Action(DeleteHistory)
  deleteHistory(
    { getState, setState }: StateContext<SearchStateModel>,
    { id }: DeleteHistory
  ): any {
    return this.searchService.deleteHistory(id).pipe(
      tap(() => {
        const state = getState();
        const filteredArray = state.history.filter(
          (item: any) => item.id !== id
        );
        setState({
          ...state,
          history: filteredArray,
        });
      })
    );
  }

  @Action(CheckHistory)
  checkHistory(
    { getState, setState }: StateContext<SearchStateModel>,
    { searchParams }: CheckHistory
  ): any {
    return this.searchService.checkHistory(searchParams).pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          selectedHistory: result,
        });
      })
    );
  }

  @Action(SaveSelectedContent)
  saveSelectedContent(
    { getState, patchState }: StateContext<SearchStateModel>,
    { payload }: SaveSelectedContent
  ): any {
    return this.searchService.saveSelectedContent(payload).pipe(
      tap((result: any) => {
        // const state = getState();
        // patchState({
        //   contents: [...state.contents, result],
        // });
      })
    );
  }
}
