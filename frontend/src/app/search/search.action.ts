export class SearchContent {
  static readonly type = '[Search] Search';

  constructor(public searchParams: {}) {}
}

export class SetSearchParams {
  static readonly type = '[Search] Set';

  constructor(public searchParams: {}) {}
}

export class GetHistory {
  static readonly type = '[History] Get';
}

export class GetContentFile {
  static readonly type = '[History] Get File';

  constructor(public filename: string) {}
}

export class DeleteHistory {
  static readonly type = '[History] Delete';

  constructor(public id: string) {}
}

export class CheckHistory {
  static readonly type = '[History] Check';

  constructor(public searchParams: {}) {}
}

export class SaveSelectedContent {
  static readonly type = '[History] Save Selected';

  constructor(public payload: any) {}
}
