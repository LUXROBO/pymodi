var con = new SimpleConsole({
	placeholder: "Enter Command",
	handleCommand: handle_command,
	autofocus: true, // if the console is to be the primary interface of the page
	storageID: "app-console", // or e.g. "simple-console-#1" or "workspace-1:javascript-console"	
});

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

	
	if(command.match(/^((import),? )?(modi)/i)){
		con.log((command.match(/^[A-Z]/) ? "MODI" : "Running PyMODI (v1.1.0)") + (command.match(/\.|!/) ? "." : ""));
	}else if(command.match(/^(reset)/i)){
		con.clear();
	}else if(command.match(/^(tutorial)/i)){
		con.clear();
		con.logHTML("Welcome to PyModi Tutorial!");
		con.logHTML("Please Enter the code 'Play'");
	}else if(command.match(/^(>?[:;8X][-o ]?[O03PCDS\\/|()[\]{}])$/i)){
		log_emoticon(command, +1);
	}else if(command.match(/^([O03PCDS\\/|()[\]{}][-o ]?[:;8X]<?)$/i)){
		log_emoticon(command, -1);
	}else if(command.match(/^<3$/i)){
		con.log("❤");
	// Unhelp
	}else if(command.match(/^(!*\?+!*|(please |plz )?(((I )?(want|need)[sz]?|display|show( me)?|view) )?(the |some )?help|^(gimme|give me|lend me) ((the |some )?)help| a hand( here)?)/i)){ // overly comprehensive, much?
		con.log("I could definitely help you if I wanted to.");
	}else{
		var err;
		try{
			var result = eval(command);
		}catch(error){
			err = error;
		}
		if(err){
			con.error(err);
		}else{
			con.log(result).classList.add("result");
		}
	}
};
