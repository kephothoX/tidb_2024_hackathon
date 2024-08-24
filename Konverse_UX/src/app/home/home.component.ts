import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment.dev';

import { AppService } from 'src/app/app.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Buffer } from 'buffer';



@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent implements OnInit {
  formData = new FormData();
  PromptResponse: any;


  constructor(
    private _appService: AppService,
    private _formBuilder: FormBuilder,
    private _router: Router,
    private _matSnackBar: MatSnackBar
  ) { }


  ngOnInit(): void {
    
  }


  
  formGroup = this._formBuilder.group({
    firstCtrl: ['', Validators.required],
  });



  promptForm = this._formBuilder.group({
    document: ['', Validators.required],
    prompt: ['', Validators.required],
  });

  ngOnSubmit(): void {
    this.formData.append('document', `${this.promptForm.value.document}`);
    this.formData.append('prompt', `${this.promptForm.value.prompt}`);

    this._appService.prompt(this.formData).subscribe((response: any) => {

      this.PromptResponse = response.response;      
    });

  }

  uploadFile(): void{

    this._appService.uploadFile(this.formData).subscribe((response: any) => {
      this._matSnackBar.open(`${ JSON.stringify(response)}`, 'Dismiss');

      console.log(response);      
    });

  }

  ngOnSummarize(data: any): void {
    this.formData.append('prompt', `${ data }`);

    this._appService.summarize(this.formData).subscribe((response: any) => {

      this.PromptResponse = response.response;      
    });

  }



  onFileChange(event: any) {
    if (event.target.files && event.target.files.length) {
      const file = event.target.files[0];

      this.formData.append('pdf_file', file);

      this.formData.append('filename', `${ file.name.replace('-', '_').split('.')[0] }`);

    }
  }


  
}