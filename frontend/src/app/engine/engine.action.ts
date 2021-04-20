export class GetEngines {
  static readonly type = '[Engine] Get';
}

export class CreateEngine {
  static readonly type = '[Engine] Create';

  constructor(public payload: any) {}
}

export class UpdateEngine {
  static readonly type = '[Engine] Update';

  constructor(public id: string, public payload: any) {}
}

export class DeleteEngine {
  static readonly type = '[Engine] Delete';

  constructor(public id: string) {}
}
