import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import { SearchContent, GetEngines, SetSearchParams } from './search.action';
import { SearchService } from './search.service';
import { tap } from 'rxjs/operators';

export class SearchStateModel {
  contents: any;
  engines: any;
  params: any;
}

@Injectable()
@State<SearchStateModel>({
  name: 'search',
  defaults: {
    contents: null,
    engines: null,
    params: null,
  },
})
export class SearchState {
  constructor(private searchService: SearchService) {}

  @Selector()
  static getContentList(state: SearchStateModel): any {
    return state.contents;
  }

  @Selector()
  static getEngineList(state: SearchStateModel): any {
    return state.engines;
  }

  @Selector()
  static getSearchParamss(state: SearchStateModel): any {
    return state.params;
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

  @Action(GetEngines)
  getEngines({ getState, setState }: StateContext<SearchStateModel>): any {
    return this.searchService.getEngines().pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          engines: result,
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
}
