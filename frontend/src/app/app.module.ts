import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomePageComponent } from './pages/home-page/home-page.component';
import { SearchFormComponent } from './components/form/search-form/search-form.component';
import { ContentTableComponent } from './components/table/content-table/content-table.component';

// PrimeNG UI Framework
import { PrimeNgModule } from './primeng.module';

// NGXS
import { NgxsModule } from '@ngxs/store';
import { NgxsReduxDevtoolsPluginModule } from '@ngxs/devtools-plugin';
import { NgxsLoggerPluginModule } from '@ngxs/logger-plugin';

// State
import { ContentState } from './search/search.state';

@NgModule({
  declarations: [AppComponent, HomePageComponent, SearchFormComponent, ContentTableComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgxsModule.forRoot([ContentState]),
    NgxsReduxDevtoolsPluginModule.forRoot(),
    NgxsLoggerPluginModule.forRoot(),
    PrimeNgModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
