import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import { SearchContent, GetEngines } from './search.action';
import { SearchService } from './search.service';
import { tap } from 'rxjs/operators';

export class ContentStateModel {
  contents: any;
  engines: any;
}

@Injectable()
@State<ContentStateModel>({
  name: 'content',
  defaults: {
    contents: null,
    engines: null,
  },
})
export class ContentState {
  constructor(private searchService: SearchService) {}

  @Selector()
  static getContentList(state: ContentStateModel): any {
    return state.contents;
  }

  @Selector()
  static getEngineList(state: ContentStateModel): any {
    return state.engines;
  }

  @Action(SearchContent)
  searchContent(
    { getState, setState }: StateContext<ContentStateModel>,
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
  getEngines({ getState, setState }: StateContext<ContentStateModel>): any {
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
}
