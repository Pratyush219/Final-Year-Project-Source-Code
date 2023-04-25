import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FrontviewComponent } from './pages/frontview/frontview.component';

const routes: Routes = [
  {path:'',component:FrontviewComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
