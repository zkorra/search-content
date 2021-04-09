import { Injectable } from '@angular/core';
import { State, Action, StateContext, Selector } from '@ngxs/store';
import {
  GetEngines,
  CreateEngine,
  UpdateEngine,
  DeleteEngine,
} from './engine.action';
import { EngineService } from './engine.service';
import { tap } from 'rxjs/operators';

export class EngineStateModel {
  engines: any;
}

@Injectable()
@State<EngineStateModel>({
  name: 'engine',
  defaults: {
    engines: null,
  },
})
export class EngineState {
  constructor(private engineService: EngineService) {}

  @Selector()
  static getEngineList(state: EngineStateModel): any {
    return state.engines;
  }

  @Action(GetEngines)
  getEngines({ getState, setState }: StateContext<EngineStateModel>): any {
    return this.engineService.getEngines().pipe(
      tap((result) => {
        const state = getState();
        setState({
          ...state,
          engines: result,
        });
      })
    );
  }

  @Action(CreateEngine)
  createEngine(
    { getState, patchState }: StateContext<EngineStateModel>,
    { payload }: CreateEngine
  ): any {
    return this.engineService.createEngine(payload).pipe(
      tap((result: any) => {
        const state = getState();
        patchState({
          engines: [...state.engines, result],
        });
      })
    );
  }

  @Action(UpdateEngine)
  updateCategory(
    { getState, setState }: StateContext<EngineStateModel>,
    { id, payload }: UpdateEngine
  ): any {
    return this.engineService.updateEngine(id, payload).pipe(
      tap((result: any) => {
        const state = getState();
        const engineList = [...state.engines];
        const engineIndex = engineList.findIndex(
          (item) => item.searchEngineId === payload.searchEngineId
        );
        engineList[engineIndex] = result;
        setState({
          ...state,
          engines: engineList,
        });
      })
    );
  }

  @Action(DeleteEngine)
  deleteEngine(
    { getState, setState }: StateContext<EngineStateModel>,
    { id }: DeleteEngine
  ): any {
    return this.engineService.deleteEngine(id).pipe(
      tap(() => {
        const state = getState();
        const filteredArray = state.engines.filter(
          (item: any) => item.id !== id
        );
        setState({
          ...state,
          engines: filteredArray,
        });
      })
    );
  }
}
