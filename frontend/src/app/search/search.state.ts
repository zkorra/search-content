import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import { SearchContent } from './search.action';
import { SearchService } from './search.service';
import { tap } from 'rxjs/operators';

export class ContentStateModel {
  content: any;
}

@Injectable()
@State<ContentStateModel>({
  name: 'content',
  defaults: {
    content: null,
  },
})
export class ContentState {
  constructor(private searchService: SearchService) {}

  @Selector()
  static getContent(state: ContentStateModel): any {
    return state.content;
  }

  @Action(SearchContent)
  searchContent(
    { getState, setState }: StateContext<ContentStateModel>,
    { userParams }: SearchContent
  ): any {
    return this.searchService.fetchCustomSearch(userParams).pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          content: result,
        });
      })
    );
  }
}
