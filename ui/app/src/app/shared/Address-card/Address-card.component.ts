import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Address-card.component.html',
  styleUrls: ['./Address-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Address-card]': 'true'
  }
})

export class AddressCardComponent {


}