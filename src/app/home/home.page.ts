import { Component } from '@angular/core';
import { Camera, CameraOptions } from '@ionic-native/camera/ngx';
import { TextToSpeech } from '@ionic-native/text-to-speech/ngx';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { RequestOptions } from '@angular/http';
import Speech from 'speak-tts';
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  currentImage: string;
  pokemon = "Pikachu" //get from flask
  choice: string; //send to flask
  constructor(private camera: Camera,
    private tts: TextToSpeech,
    private http: HttpClient,
    private speech: Speech) {

    if (speech.hasBrowserSupport()) { // returns a boolean
      console.log("speech synthesis supported");
    }
    this.speech.init().then((data) => {
      // The "data" object contains the list of available voices and the voice synthesis params
      //console.log("Speech is ready, voices are available", data)

    }).catch(e => {
      console.error("An error occured while initializing : ", e)
    })

  }
  onChoice() {
    this.currentImage = "/../assets/SamplePokemon/" + this.choice + ".png";
    //this.sendPokemon()
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
  playCry() {
    let audio = new Audio();
    audio.src = "/../assets/sounds/" + this.pokemon + ".wav";
    audio.load();
    audio.play();
  }
  // playtts() {
  //   this.tts.speak('Hello World')
  //     .then(() => console.log('Success'))
  //     .catch((reason: any) => console.log(reason));
  // }
  // getPokemon() {
  //   try{
  //   this.http.get('http://127.0.0.1:5000/').subscribe((response) => {
  //     console.log(response);
  //     this.pokemon = response;
  //     this.readEntry();
  //   });
  // }catch{}
  // }
  sendPokemon() {
    var headers = new HttpHeaders();
    headers.append("Accept", 'application/json');
    headers.append('Content-Type', 'application/json');
    const requestOptions = new RequestOptions({ headers: headers });

    let postData = {
      "pokemon": this.choice
    }

    this.http.post('http://127.0.0.1:5000/', postData, requestOptions)
      .subscribe(data => {
        console.log(data['_body']);
      }, error => {
        console.log(error);
      });
  }
  readEntry() {
    this.speech.speak({
      text: this.getEntry(),
    }).then(() => {
      console.log("Success !")
    }).catch(e => {
      console.error("An error occurred :", e)
    })
  }

  getEntry() {
    let pikachuEntries = [
      "When several of these Pokémon gather, their electricity could build and cause lightning storms.",
      "It keeps its tail raised to monitor its surroundings. If you yank its tail, it will try to bite you.",
      "Lives in forests away from people. It stores electricity in its cheeks for zapping an enemy if it is attacked.",
      "This intelligent Pokémon roasts hard berries with electricity to make them tender enough to eat.",
      "It raises its tail to check its surroundings. The tail is sometimes struck by lightning in this pose.",
      "When it is angered, it immediately discharges the energy stored in the pouches in its cheeks.",
      "This intelligent Pokémon roasts hard Berries with electricity to make them tender enough to eat.",
      "Whenever Pikachu comes across something new, it blasts it with a jolt of electricity. If you come across a blackened berry, it's evidence that this Pokémon mistook the intensity of its charge.",
      "This Pokémon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pikachu sleeps. It occasionally discharges electricity when it is dozy after waking up.",
      "It stores electricity in the electric sacs on its cheeks. When it releases pent-up energy in a burst, the electric power is equal to a lightning bolt.",
      "It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.",
      "When several of these Pokémon gather, their electricity could build and cause lightning storms.",
      "It lives in forests with others. It stores electricity in the pouches on its cheeks.",
      "If it looses crackling power from the electrical pouches on its cheeks, it is being wary.",
      "It occasionally uses an electric shock to recharge a fellow Pikachu that is in a weakened state.",
      "This intelligent Pokémon roasts hard berries with electricity to make them tender enough to eat.",
      "It raises its tail to check its surroundings. The tail is sometimes struck by lightning in this pose.",
      "It occasionally uses an electric shock to recharge a fellow Pikachu that is in a weakened state.",
      "It raises its tail to check its surroundings. The tail is sometimes struck by lightning in this pose.",
      "It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs.",
      "Whenever Pikachu comes across something new, it blasts it with a jolt of electricity. If you come across a blackened berry, it's evidence that this Pokémon mistook the intensity of its charge.",
      "This Pokémon has electricity-storing pouches on its cheeks. These appear to become electrically charged during the night while Pikachu sleeps. It occasionally discharges electricity when it is dozy after waking up.",
      "A plan was recently announced to gather many Pikachu and make an electric power plant.",
      "It's in its nature to store electricity. It feels stressed now and then if it's unable to fully discharge the electricity.",
      "Its nature is to store up electricity. Forests where nests of Pikachu live are dangerous, since the trees are so often struck by lightning.",
      "While sleeping, it generates electricity in the sacs in its cheeks. If it's not getting enough sleep, it will be able to use only weak electricity.",
      "This forest-dwelling Pokémon stores electricity in its cheeks, so you'll feel a tingly shock if you touch it."]
    let squirtleEntries = [
      "After birth, its back swells and hardens into a shell. Powerfully sprays foam from its mouth.",
      "Shoots water at prey while in the water. Withdraws into its shell when in danger.",
      "It takes time for the shell to form and harden after hatching. It sprays foam powerfully from its mouth.",
      "The shell is soft when it is born. It soon becomes so resilient, prodding fingers will bounce off it.",
      "The shell, which hardens soon after it is born, is resilient. If you poke it, it will bounce back out.",
      "When it feels threatened, it draws its legs inside its shell and sprays water from its mouth.",
      "Squirtle's shell is not merely used for protection. The shell's rounded shape and the grooves on its surface help minimize resistance in water, enabling this Pokémon to swim at high speeds.",
      "Its shell is not just for protection. Its rounded shape and the grooves on its surface minimize resistance in water, enabling Squirtle to swim at high speeds.",
      "When it retracts its long neck into its shell, it squirts out water with vigorous force.",
      "After birth, its back swells and hardens into a shell. Powerfully sprays foam from its mouth.",
      "It shelters itself in its shell, then strikes back with spouts of water at every opportunity.",
      "Shoots water at prey while in the water. Withdraws into its shell when in danger.",
      "Squirtle's shell is not merely used for protection. The shell's rounded shape and the grooves on its surface help minimize resistance in water, enabling this Pokémon to swim at high speeds.",
    ]
    let bulbasaurEntries = [
      "A strange seed was planted on its back at birth. The plant sprouts and grows with this Pokémon.",
      "It can go for days without eating a single morsel. In the bulb on its back, it stores energy.",
      "The bulb-like pouch on its back grows larger as it ages. The pouch is filled with numerous seeds.",
      "The seed on its back is filled with nutrients. The seed grows steadily larger as its body grows.",
      "It carries a seed on its back right from birth. As it grows older, the seed also grows larger.",
      "While it is young, it uses the nutrients that are stored in the seeds on its back in order to grow.",
      "There is a plant seed on its back right from the day this Pokémon is born. The seed slowly grows larger.",
      "For some time after its birth, it grows by gaining nourishment from the seed on its back.",
      "Bulbasaur can be seen napping in bright sunlight. There is a seed on its back. By soaking up the sun's rays, the seed grows progressively larger.",
      "It can go for days without eating a single morsel. In the bulb on its back, it stores energy."
    ]
    let charmanderEntries = [
      "Obviously prefers hot places. When it rains, steam is said to spout from the tip of its tail.",
      "The flame at the tip of its tail makes a sound as it burns. You can only hear it in quiet places.",
      "Even the newborns have flaming tails. Unfamiliar with fire, babies are said to accidentally burn themselves.",
      "The flame on its tail indicates Charmander's life force. If it is healthy, the flame burns brightly.",
      "If it's healthy, the flame on the tip of its tail will burn vigorously, even if it gets a bit wet.",
      "The flame that burns at the tip of its tail is an indication of its emotions. The flame wavers when Charmander is enjoying itself. If the Pokémon becomes enraged, the flame burns fiercely.",
      "The flame that burns at the tip of its tail is an indication of its emotions. The flame wavers when Charmander is happy, and blazes when it is enraged.",
      "It has a preference for hot things. When it rains, steam is said to spout from the tip of its tail.",
      "The fire on the tip of its tail is a measure of its life. If healthy, its tail burns intensely.",
      "The flame on its tail shows the strength of its life force. If it is weak, the flame also burns weakly.",
      "The flame on its tail indicates Charmander's life force. If it is healthy, the flame burns brightly.",
      "From the time it is born, a flame burns at the tip of its tail. Its life would end if the flame were to go out.",
      "The flame at the tip of its tail makes a sound as it burns. You can only hear it in quiet places.",
    ]
    let random = 0;
    switch (this.pokemon) {
      case "Pikachu":
        random = Math.floor(Math.random() * pikachuEntries.length)
        return "Pikachu: the Mouse Pokémon. " + pikachuEntries[random]
        break;
      case "Bulbasaur":
        random = Math.floor(Math.random() * bulbasaurEntries.length)
        return "Bulbasaur: the Seed Pokémon. " + bulbasaurEntries[random]
        break;
      case "Charmander":
        random = Math.floor(Math.random() * charmanderEntries.length)
        return "Charmander: the Lizard Pokemon. " + charmanderEntries[random]
        break;
      case "Squirtle":
        random = Math.floor(Math.random() * squirtleEntries.length)
        return "Squirtle: the Tiny Turtle Pokémon. " + squirtleEntries[random]
        break;
      default:
        return "Unknown Pokemon";
    }
  }
}
