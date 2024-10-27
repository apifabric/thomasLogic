import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CustomerReview-card.component.html',
  styleUrls: ['./CustomerReview-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CustomerReview-card]': 'true'
  }
})

export class CustomerReviewCardComponent {


}