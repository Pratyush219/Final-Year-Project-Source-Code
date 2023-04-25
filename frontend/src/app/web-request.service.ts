import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class WebRequestService{
  readonly ROOT_URL;
  constructor(private http:HttpClient) {
    this.ROOT_URL='D:/Projects/Final-Year-Project-Source/data';
  }

  get(uri:string){
    return this.http.get(`${this.ROOT_URL}/${uri}`);
  } 
  
  post(uri:string,payload:Object){
    
  }

}
