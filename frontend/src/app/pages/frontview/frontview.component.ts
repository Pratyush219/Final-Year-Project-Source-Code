import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params, Router } from '@angular/router';
import { TaskService } from 'src/app/task.service';
import { WebRequestService } from 'src/app/web-request.service';

@Component({
  selector: 'app-frontview',
  templateUrl: './frontview.component.html',
  styleUrls: ['./frontview.component.scss']
})
export class FrontviewComponent implements OnInit {
  csvFiles:any;
  constructor(private taskService:TaskService,private route:ActivatedRoute,private router:Router){}
  
  ngOnInit(){
    this.taskService.getCsvFiles().subscribe((files:any)=>{
      this.csvFiles=files;
    });
  }

}
