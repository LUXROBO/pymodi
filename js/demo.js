//img drag & drop part
window.console = window.console || function(t) {};

if (document.location.search.match(/type=embed/gi)) {
	window.parent.postMessage("resize", "*");
}

let id = [];

function allowDrop(event) {
	event.preventDefault();
}
	
function drag(event) {
	event.dataTransfer.setData("text", event.target.id);
	}

function drop(event) {
	event.preventDefault();
	var data = event.dataTransfer.getData("text");
	
	var nodeCopy = document.getElementById(data).cloneNode(true);
	
	if (nodeCopy.id.match("[0]")) {}
	else nodeCopy.id += "[0]";

	if(nodeCopy.id == "network[0]" || nodeCopy.id == "button[0]" || nodeCopy.id == "led[0]")
	{
		id.push(nodeCopy.id);
	}
	event.target.appendChild(nodeCopy);
		if (event.target == document.getElementById("dropBox1")) {
			var trs = document.getElementById(data);
			trs.parentNode.removeChild(trs);

		}
}

//js console part
var con = new SimpleConsole({
	placeholder: "Enter Command",
	handleCommand: handle_command,
	autofocus: true, // if the console is to be the primary interface of the page
	storageID: "app-console", // or e.g. "simple-console-#1" or "workspace-1:javascript-console"	
});

var lesson_ = 0; // key value of keyword'Next'
var pass_ = 0;
var button_pressed = 0;
var input_code = 0;
var error_count = 0;
var error_number = 0;
var is_module_all = 0;
var button_toggle = 0; // 0: noclick 1:click
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

};

function play_page() {
	con.logHTML("Tutorial includes :");
	con.logHTML("1. Making MODI");
	con.logHTML("2. Accessing Modules");
	con.logHTML("3. Controlling Modules");
	con.logHTML("4. PyMODI Project");
	con.logHTML("");
	con.logHTML("Enter command the lesson number and press ENTER");
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
	con.logHTML("Press ENTER");
};

function importMODI_reaction2() {
	con.logHTML("");
	if(id.indexOf("network[0]") != -1 && id.indexOf("button[0]") != -1 && id.indexOf("led[0]") != -1){
		con.log("modules are connected!");
		con.logHTML("");
		importMODI_reaction3();
		is_module_all = 1;
	}
	else{
		let need_id = [];
		if(id.indexOf("network[0]") == -1) {
			need_id.push("network");
		} 
		if(id.indexOf("button[0]") == -1) {
			need_id.push("button");
		}
		if(id.indexOf("led[0]") == -1) {
			need_id.push("led");
		}
		if(need_id != null) {
			con.log(need_id);
			con.log("Modules not connected!");
			con.log("");
		}

		con.logHTML("If you haven't moved the module yet, Please drag Network, Button, LED module and drop at the centor area.");
		con.logHTML("If you're ready, press ENTER");
	};
};

function importMODI_reaction3() {
	con.logHTML("Next, Make a MODI bundle object by typing bundle = modi.MODI()");
	con.logHTML("Enter Command : bundle = modi.MODI()");
}
function bundle_modi() {
	con.logHTML("Start initializing connected MODI modules");
	con.logHTML("Network (1761) has been connected!");
	con.logHTML("Button (3718) has been connected!");
	con.logHTML("Led (2931) has been connected!");
	con.logHTML("MODI modules are initialized!");
	con.logHTML("");
	con.logHTML('Great! The "bundle" is your MODI object. With it, you can control all the modules connected to your device.');
	con.logHTML("");
	con.logHTML("You have completed this lesson. Press ENTER to continue.");
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
	con.logHTML("You have completed this lesson. Press ENTER to continue.");
	lesson_ = 3;
};

function Controlling_modules() {
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Lesson 3: Controlling modules");
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("Now you know how to access individual modules. Let's make an object named 'button' as well for your button module. You know how to do it (You have the modi object, 'bundle').");
	error_count = 1;
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
	con.logHTML("You can press the button by clicking on the button where in the centor area.");
	con.logHTML("Type button.pressed, after press the button.");
	Button_press();
};

function Controlling_modules4() {
	con.logHTML("");
	con.logHTML("Good. if you click the button one more, the button's state return 'not pressed'.");
	con.logHTML("Now let's send a command to the led module. Led's rgb is a property or setter method of an led module.");
	con.logHTML("Let there be light by typing led.rgb = 0, 0, 100");
	con.logHTML("led.rgb = 0, 0, 100");
};

function Controlling_modules5() {
	con.logHTML("");
	con.logHTML("Perfect! You will see the blue light from the LED module.");
	con.logHTML("if you want to turn off the led, this code let you what you want.")
	con.logHTML("led.rgb = 0, 0, 0");
};

function Controlling_modules6() {
	con.logHTML("");
	con.logHTML("You have completed this lesson. Press ENTER to continue.");
	lesson_ = 4;
}

function Pymodi_project() {
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Lesson 4: Your First PyMODI Project");
	con.logHTML("--------------------------------------------------------------------");
	con.logHTML("Let's make a project that blinks led when button 'is pressed'.");
	con.logHTML("In an infinite loop, we want our led to light up");
	con.logHTML("when button is pressed, and turn off when not pressed. Complete the following code based on the description.");
	con.logHTML("");
	con.logHTML("");
	con.logHTML("Press ENTER when you're ready!");
	lesson_ = 6;
}

function Pymodi_project2() {
	con.logHTML("while True:");
	con.logHTML(". . .&emsp;&emsp;# Check if button is pressed");
	con.input.value = ". . .       if ";
}

function Pymodi_project3() {
	con.logHTML("Congrats!! Now let's see if the code works as we want. Press the button to light up the led. Double click the button to break out of the loop.");
	Play_project();
}

function Pymodi_project4() {
	con.logHTML("It looks great!");
	con.logHTML("Now you know how to use PyMODI to control modules.");
	con.logHTML("You can look up more functions at this site!");
	con.logHTML("");
	con.logHTML("");
	con.logHTML("You have completed the tutorial.");

}

function Play_project() {
	var img = document.getElementById("button[0]");

	img.onclick = function(){
		if (button_toggle == 1 )
		{
			img.src = "assets/img/demo-modules/button.png";
			document.getElementById("led[0]").src = "assets/img/demo-modules/led.png";	
			button_toggle = 0;
		}
		else if (button_toggle == 0)
		{
			img.src = "assets/img/demo-modules/button_click.png";
			document.getElementById("led[0]").src = "assets/img/demo-modules/led_green.png";
			button_toggle = 1;
		}
	};
}

function Button_press() {
	var imgs = document.getElementById("button[0]");


	imgs.onclick = function(){
		if (button_toggle == 1)
		{
			imgs.src = "assets/img/demo-modules/button.png";	
			button_toggle = 0;
		}
		else if (button_toggle == 0)
		{
 			imgs.src = "assets/img/demo-modules/button_click.png";	
			button_toggle = 1;
		}
	};
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


	// press enter to next lesson
	if (command == ""){ 
		if(lesson_ == 1 && is_module_all == 0){
			con.clear();
			importMODI_reaction2();

		}
		else if(lesson_ == 2){
			con.clear();
			Accessing_module();
			lesson_ = 0;
		}
		else if(lesson_ == 3){
			con.clear();
			Controlling_modules();
			lesson_ = 0;
		}
		else if(lesson_ ==4){
			con.clear();
			Pymodi_project();
		}
		else if(lesson_ == 6){
			con.clear();
			Pymodi_project2();
			lesson_ = 5;
		}
	} 
	// command process
	else {
		if (command == "import modi") {
			con.log((command.match(/^[A-Z]/) ? "MODI" : "Running PyMODI (v1.1.0)") + (command.match(/\.|!/) ? "." : ""));
			importMODI_reaction();
		} else if (command.match(/^(reset)/i)) {
			con.clear();
			lesson_ = 0;
			pass_ = 0;
			button_pressed = 0;
			input_code = 0;
		} else if (command == "tutorial") {
			lesson_ = 0;
			pass_ = 0;
			button_pressed = 0;
			input_code = 0;
			con.clear();
			intro_page();

		} else if (command == "play") {
			con.clear();
			play_page();
		} else if (command == "1") {
			con.clear();
			makingMODI_page();
		} else if (command == "2") { 
			con.clear();
			Accessing_module();
		} else if (command == "3") { 
			con.clear();
			Controlling_modules();
		} else if (command == "4") { 
			con.clear();
			Pymodi_project();
		} else if (command == "bundle = modi.MODI()") {
			bundle_modi();
		} else if (!command.match(". . .               led.rgb = 0, 100, 0") && input_code == 1) {
			con.log("Try again! the answer is 'led.rgb = 0, 100, 0'. Type it below.");
			con.input.value = ". . .               ";
		} else if (command.match(". . .               led.rgb = 0, 100, 0") && input_code == 1) {
			input_code += 1;
			con.logHTML(". . .&emsp;&emsp;elif button.double_clicked:");
			con.logHTML(". . .&emsp;&emsp;&emsp;&emsp;break");
			con.logHTML(". . .&emsp;&emsp;else:");
			con.logHTML(". . .&emsp;&emsp;&emsp;&emsp;# Turn off the led. (i.e. set color to (0, 0, 0))");
			con.input.value = ". . .               ";
		} else if (!command.match(". . .               led.rgb = 0, 0, 0") && input_code == 2) {
			con.log("Try again! the answer is 'led.rgb = 0, 0, 0'. Type it below.");
			con.input.value = ". . .               ";
		} else if (command.match(". . .               led.rgb = 0, 0, 0") && input_code == 2) {
			Pymodi_project3();
		} else if (lesson_ == 5){
			if (!command.match(". . .       if button.pressed:") && input_code == 0) {
				con.log("Try again! the answer is 'button.pressed:'. Type it below.");
				con.input.value = ". . .       if ";
			}
			else {
				input_code += 1;
				con.logHTML(". . .&emsp;&emsp;&emsp;&emsp;# Set Led color to green");
				con.input.value = ". . .               ";
			}
		} else if (command == "bundle.modules") {
			Accessing_module2();
		} else if (command == "bundle.leds") {
				Accessing_module3();
		} else if (command == "led = bundle.leds[0]") {
			Accessing_module4();
		} else if (command != "button = bundle.buttons[0]" && error_count > 0) {
			if (error_count == 1){
				con.log("Try again!");
				error_count++;
			}
			else if(error_count > 1) {
				con.log("The answer is 'button = bundle.buttons[0]'. Type it below.")
				error_count++;
			}
		} else if (command == "button = bundle.buttons[0]") {
			error_count = 0;
			Controlling_modules2();

		} else if (command == "button.pressed") {
			if (button_toggle == 0)
			{
				con.log("False");
				Controlling_modules3();
				//button_pressed = 1;
			}
			else if (button_toggle == 1)
			{
				con.log("True");
				Controlling_modules4();
				//button_pressed = 0;
			}
			
		} else if (command == "led.rgb = 0, 0, 100") {
			document.getElementById("led[0]").src = "assets/img/demo-modules/led_blue.png";
			Controlling_modules5();
		} else if (command == "led.rgb = 0, 0, 0") {
			document.getElementById("led[0]").src = "assets/img/demo-modules/led.png";
			Controlling_modules6();
		} else if (command.match("0") || command.match("1") || command.match("2") || command.match("3") || command.match("4") || command.match("5") || command.match("6") || command.match("7") || command.match("8") || command.match("9")) {
			con.log("Try again!");
		} else {
			var err;
			try{
				var result = eval(command);
			}catch(error) {
				err = error;
			}
			if(err) {
				con.error(err);
			} else {
				con.log(result).classList.add("result");
			}
		}
	}
};
