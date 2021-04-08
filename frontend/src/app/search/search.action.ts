export class SearchContent {
  static readonly type = '[Search] Search';

  constructor(public searchParams: {}) {}
}

export class GetEngines {
  static readonly type = '[Search] Engines';
}

export class SetSearchParams {
  static readonly type = '[Search] Set';

  constructor(public searchParams: {}) {}
}
