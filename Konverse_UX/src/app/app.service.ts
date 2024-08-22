import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { environment } from 'src/environments/environment.dev';

import { ErrorService } from './error/error.service';
import { Observable, catchError, of} from 'rxjs';

import { MatSnackBar } from '@angular/material/snack-bar';



@Injectable({
  providedIn: 'root'
})
export class AppService {

  constructor(
    private _errorService: ErrorService,
    private _httpClient: HttpClient,
    private _matSnackBar: MatSnackBar
  ) {  }

  httpOptionsMultipartForm = {
    headers: new HttpHeaders({
      'Content-Type': 'multipart/form-data; boundary=---Konverse',
    }),
    response: 'json'
  }

  httpOptionsPlainForm = {
    headers: new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    }),
    response: 'json'
  }


  APIEndpoint = environment.APIEndpoint;




  
  
}
