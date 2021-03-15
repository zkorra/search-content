import { Component, OnInit } from '@angular/core';

import { ContentState } from '../../search/search.state';
import { SearchContent } from '../../search/search.action';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.scss'],
})
export class HomePageComponent implements OnInit {
  @Select(ContentState.getContent)
  content: any;

  userParams = {
    type: 'article',
    cx: '07f7a2e8b0b662f50',
    query: 'python',
    // page: '',
    // region: '',
  };

  cols: any[] = [];

  constructor(private store: Store) {}

  async ngOnInit(): Promise<void> {
    await this.store.dispatch(new SearchContent(this.userParams)).toPromise();
  }
}
