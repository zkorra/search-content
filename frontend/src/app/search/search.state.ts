import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import { SearchContent } from './search.action';
import { SearchService } from './search.service';
import { tap } from 'rxjs/operators';

export class ContentStateModel {
  contentList: any;
}

@Injectable()
@State<ContentStateModel>({
  name: 'content',
  defaults: {
    contentList: null,
  },
})
export class ContentState {
  constructor(private searchService: SearchService) {}

  @Selector()
  static getContent(state: ContentStateModel): any {
    return state.contentList;
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
          contentList: result,
        });
      })
    );
  }
}
