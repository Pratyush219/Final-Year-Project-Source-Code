import { Injectable } from '@angular/core';
import { WebRequestService } from './web-request.service';

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  constructor(private webService:WebRequestService) { }

  getCsvFiles(){
    return this.webService.get('files');
  }
  
}
