var con = new SimpleConsole({
	placeholder: "Enter Command",
	handleCommand: handle_command,
	autofocus: true, // if the console is to be the primary interface of the page
	storageID: "app-console", // or e.g. "simple-console-#1" or "workspace-1:javascript-console"	
});

var lesson_ = 0; // key value of keyword'Next'
var pass_ = 0;
var button_pressed = 0;
intro_page();

// Tutorial page
function intro_page() {
	con.logHTML("========================================================");
	con.logHTML("=&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&nbsp;&nbsp;&nbsp;Welcome to PyMODI Tutorial&nbsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;=");
	con.logHTML("========================================================");
	con.logHTML("PyMODI is a very powerful tool that can control the MODI modules using python scripts. As long as you learn how to use built-in functions of PyMODI, you can easily control MODI modules. This interactive GUI tutorial will guide you through the world of PyMODI.");
	con.logHTML("");
	con.logHTML("");
	con.logHTML("Please drag Network, Button, LED module and drop at the centor area First!");
	con.logHTML("If you've succeeded in dragging and dropping all the modules, please enter the command 'play'.");
	con.logHTML("Enter Command : play");
	return "intro";
};

function play_page() {
	con.logHTML("Tutorial includes :");
	con.logHTML("1. Making MODI");
	con.logHTML("2. Accessing Modules");
	con.logHTML("3. Controlling Modules");
	con.logHTML("4. PyMODI Project");
	con.logHTML("");
	con.logHTML("Enter the lesson word");
	con.logHTML("Ex)Enter Command : Making MODI");
};

function makingMODI_page() {
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Lesson 1: Making MODI");
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("First, you should import modi.");
	con.logHTML("Enter Command : import modi");
};

function importMODI_reaction() {
	lesson_ = 1;
	con.logHTML("Great! Now you can use all the features of MODI!");
	con.logHTML("");
	con.logHTML("To control the modules, make a MODI object that contains all the connected modules. Once you create it, it will automatically find all the modules connected to the network module.");
	con.logHTML("");
	con.logHTML("Enter Command 'next'");
};

function importMODI_reaction2() {
	con.logHTML("Now, prepare real MODI modules. Connect a network module to your computing device. Then, connect a Button module and an Led module. Make a MODI bundle object by typing bundle = modi.MODI()");
	con.logHTML("Enter Command : bundle = modi.MODI()");
};

function bundle_modi() {
	con.logHTML("Start initializing connected MODI modules");
	con.logHTML("Network (1761) has been connected!");
	con.logHTML("Button (3718) has been connected!");
	con.logHTML("Led (2931) has been connected!");
	con.logHTML("MODI modules are initialized!");
	con.logHTML("");
	con.logHTML('Great! The "bundle" is your MODI object. With it, you can control all the modules connected to your device.');
	con.logHTML("");
	con.logHTML("You have completed this lesson. Enter the Command 'Next' to continue.");
	lesson_ = 2;
};

function Accessing_module() {
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Lesson 2: Accessing modules");
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("In the previous lesson, you created a MODI object. Let's figure out how we can access modules connected to it.");
	con.logHTML("");
	con.logHTML('"bundle.modules" is a method to get all the modules connected to the device.');
	con.logHTML("");
	con.logHTML("bundle.modules");
};

function Accessing_module2() {
	con.logHTML("[＜modi.module.setup_module.network.Network object at 0x0000012B42B6E288＞, ＜modi.module.output_module.led.Led object at 0x0000012B425DE8C8＞, ＜modi.module.input_module.button.Button object at 0x0000012B42B6E308＞]");
	con.logHTML("");
	con.logHTML("you can see two modules connected (excluding the network module) to the machine. You can access each module by the same method we use with an array.");
	con.logHTML("You can also access modules by types.");
	con.logHTML("");
	con.logHTML("bundle.leds");
};

function Accessing_module3() {
	con.logHTML("[＜modi.module.output_module.led.Led object at 0x0000012B425DE8C8＞]");
	con.logHTML("");
	con.logHTML("If you have followed previous instructions correctly, there must be one led module connected to the network module. Now, make an led variable by accessing the first led module.");
	con.logHTML("");
	con.logHTML("led = bundle.leds[0]");
	pass_ = 1;
};

function Accessing_module4() {
	con.logHTML("Super! You can now do whatever you want with these modules. If you have different modules connected, you can access the modules in a same way, just typing bundle");
	con.logHTML("");
	con.logHTML("You have completed this lesson. Enter the Command 'Next' to continue.");
	lesson_ = 3;
};

function Controlling_modules() {
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Lesson 3: Controlling modules");
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("Now you know how to access individual modules. Let's make an object named 'button' as well for your button module. You know how to do it (You have the modi object, 'bundle').");
};

function Controlling_modules2() {
	con.logHTML("");
	con.logHTML("Perfect. With your button module and led module, we can either get data from the module or send command to the module.");
	con.logHTML("");
	con.logHTML('"pressed" is a property method of a button module which returns whether the button is pressed or not (i.e. press state).');
	con.logHTML("Check the press state of the button by typing button.pressed");
	con.logHTML("button.pressed");
};

function Controlling_modules3() {
	con.logHTML("");
	con.logHTML("Now, see if the same command returns True when pressing the button.");
};

function Controlling_modules4() {
	con.logHTML("");
	con.logHTML("Good. Now let's send a command to the led module. Led's rgb is a property or setter method of an led module.");
	con.logHTML("Let there be light by typing led.rgb = 0, 0, 100");
	con.logHTML("led.rgb = 0, 0, 100");
};

function Controlling_modules5() {
	con.logHTML("");
	con.logHTML("Nice! if you want to turn off the led, this code let you what you want.")
	con.logHTML("led.rgb = 0, 0, 0");
};

function Controlling_modules6() {
	con.logHTML("");
	con.logHTML("You have completed this lesson. Enter the Command 'Next' to continue.");
	lesson_ = 4;
}

// add the console to the page
document.body.appendChild(con.element);

// show any uncaught errors (errors may be unrelated to the console usage)
con.handleUncaughtErrors();

function handle_command(command){
	// Conversational trivialities
	var log_emoticon = function(face, rotate_direction){
		// top notch emotional mirroring (*basically* artificial general intelligence :P)
		var span = document.createElement("span");
		span.style.display = "inline-block";
		span.style.transform = "rotate(" + (rotate_direction / 4) + "turn)";
		span.style.cursor = "vertical-text";
		span.style.fontSize = "1.3em";
		span.innerText = face.replace(">", "〉").replace("<", "〈");
		con.log(span);
	};

	
	if (command.match(/^((import),? )?(modi)/i)){
		con.log((command.match(/^[A-Z]/) ? "MODI" : "Running PyMODI (v1.1.0)") + (command.match(/\.|!/) ? "." : ""));
		importMODI_reaction();
	} else if (command.match(/^(reset)/i)){
		con.clear();
	} else if (command.match(/^(tutorial)/i)){
		con.clear();
		intro_page();
	} else if (command.match(/^(play)/i)){
		con.clear();
		play_page();
	} else if (command.match(/^((making),? )?(modi)/i)){
		con.clear();
		makingMODI_page();
	} else if (command.match(/^((accessing),? )?(modules)/i)){ 
		con.clear();
		Accessing_module();
	} else if (command.match(/^((controlling),? )?(modules)/i)){ 
		con.clear();
		Controlling_modules();
	} else if (command.match("next")){
		if(lesson_ == 1){ // lesson 1 ing
			con.clear();
			importMODI_reaction2();
		}
		else if(lesson_ == 2){// page lesson 1 to 2
			con.clear();
			Accessing_module();
		}
		else if(lesson_ == 3){
			con.clear();
			Controlling_modules();
		}
	} else if (command.match(/^((((bundle),? ),?=),? )?(modi.MODI)/i)){
		bundle_modi();
	} else if (command.match("bundle.modules")){
		Accessing_module2();
	} else if (command.match("bundle.leds")){ // []인식 불가로 임시로 pass라는 key를 이용하여 대처
		if(pass_ == 0)
		{
			Accessing_module3();
		}
		else if (pass_ == 1)
		{
			Accessing_module4();
			pass_ = 0;
		}
	} else if (command.match("button = bundle.buttons")){
		Controlling_modules2();
	} else if (command.match("button.pressed")){
		if (button_pressed == 0)
		{
			con.log("False");
			Controlling_modules3();
			button_pressed = 1;
		}
		else if (button_pressed == 1)
		{
			con.log("True");
			Controlling_modules4();
			button_pressed = 0;
		}
		
	} else if (command.match("led.rgb = 0, 0, 100")){
		Controlling_modules5();
	} else if (command.match("led.rgb = 0, 0, 0")){
		Controlling_modules6();
	} else {
		var err;
		try{
			var result = eval(command);
		}catch(error){
			err = error;
		}
		if(err){
			con.error(err);
		} else {
			con.log(result).classList.add("result");
		}
	}
};
