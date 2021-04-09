export class SearchContent {
  static readonly type = '[Search] Search';

  constructor(public searchParams: {}) {}
}

export class SetSearchParams {
  static readonly type = '[Search] Set';

  constructor(public searchParams: {}) {}
}
