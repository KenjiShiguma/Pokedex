import { Component } from '@angular/core';
import { Camera, CameraOptions } from '@ionic-native/camera/ngx';
import { TextToSpeech } from '@ionic-native/text-to-speech/ngx';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  currentImage: any;

  constructor(private camera: Camera,private tts: TextToSpeech, private http: HttpClient) {
    this.tts.speak('Hello World')
    .then(() => console.log('Success'))
    .catch((reason: any) => console.log(reason));
    this.http.get('http://127.0.0.1:5000/').subscribe((response) => {
    console.log(response);
});

  }

  takePicture() {
    const options: CameraOptions = {
      quality: 100,
      destinationType: this.camera.DestinationType.DATA_URL,
      saveToPhotoAlbum: true,
      mediaType: this.camera.MediaType.PICTURE
    }

    this.camera.getPicture(options).then((imageData) => {
      this.currentImage = 'data:image/jpeg;base64,' + imageData;
      }, (err) => {

      });
  }
}
