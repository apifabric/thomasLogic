import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Inventory-card.component.html',
  styleUrls: ['./Inventory-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Inventory-card]': 'true'
  }
})

export class InventoryCardComponent {


}