import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';
import { Camera } from '@ionic-native/camera/ngx';
import { IonicModule, IonicRouteStrategy } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { HttpModule } from '@angular/http';
import { AppRoutingModule } from './app-routing.module';
import { TextToSpeech } from '@ionic-native/text-to-speech/ngx';
import { NativeAudio } from '@ionic-native/native-audio/ngx';
import  Speech  from 'speak-tts';


@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [BrowserModule, IonicModule.forRoot(), AppRoutingModule, HttpClientModule],
  providers: [
    StatusBar,
    SplashScreen,
    Camera,
    NativeAudio,
    HttpModule,
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    TextToSpeech,
    Speech,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
