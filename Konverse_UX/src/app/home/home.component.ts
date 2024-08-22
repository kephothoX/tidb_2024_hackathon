import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment.dev';


import { MatSnackBar } from '@angular/material/snack-bar';
import { Buffer } from 'buffer';





declare global {
  interface Window {
    ethereum: any
  }
}


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {


  constructor(
    private _matSnackBar: MatSnackBar
  ) { }


  async ngOnInit() {

    

  }

  
}