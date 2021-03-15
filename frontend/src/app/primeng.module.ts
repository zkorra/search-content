import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { OrderListModule } from 'primeng/orderlist';
import { DataViewModule } from 'primeng/dataview';
import { AutoCompleteModule } from 'primeng/autocomplete';
import { DialogModule } from 'primeng/dialog';
import { DividerModule } from 'primeng/divider';
import { CardModule } from 'primeng/card';
import { TableModule } from 'primeng/table';

@NgModule({
  imports: [CommonModule],
  exports: [
    MenubarModule,
    InputTextModule,
    ButtonModule,
    OrderListModule,
    DataViewModule,
    AutoCompleteModule,
    DialogModule,
    DividerModule,
    CardModule,
    TableModule,
  ],
})
export class PrimeNgModule {}
