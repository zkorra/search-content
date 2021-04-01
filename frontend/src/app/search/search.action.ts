export class SearchContent {
  static readonly type = '[Content] Search';

  constructor(public searchParams: {}) {}
}

export class GetEngines {
  static readonly type = '[Content] Engines';
}

export class SetSearchParams {
  static readonly type = '[Category] Set';

  constructor(public searchParams: {}) {}
}
