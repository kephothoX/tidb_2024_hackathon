import { Component, OnInit } from '@angular/core';

import { AuthService } from '@auth0/auth0-angular';


@Component({
  selector: 'app-authn',
  templateUrl: './authn.component.html',
  styleUrls: ['./authn.component.scss'],
})
export class AuthnComponent implements OnInit {
  User: any;
  isAuthenticated!: boolean;
  isAuthenticated$ = this._auth0Service.isAuthenticated$
  
  constructor (
    public  _auth0Service: AuthService
    ) {}

  ngOnInit(): void {
       

  }
}

