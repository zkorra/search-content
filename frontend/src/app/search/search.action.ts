export class SearchContent {
  static readonly type = '[Content] Search';

  constructor(public searchParams: {}) {}
}

export class GetEngines {
  static readonly type = '[Content] Engines';
}
