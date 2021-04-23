import { Component } from '@angular/core';
import {
  actionsExecuting,
  ActionsExecuting,
} from '@ngxs-labs/actions-executing';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import {
  SearchContent,
  GetHistory,
  GetContentFile,
  DeleteHistory,
  SaveSelectedContent,
} from './search/search.action';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  @Select(
    actionsExecuting([
      SearchContent,
      GetHistory,
      GetContentFile,
      DeleteHistory,
      SaveSelectedContent,
    ])
  )
  ActionsIsExecuting$!: Observable<ActionsExecuting>;
}
