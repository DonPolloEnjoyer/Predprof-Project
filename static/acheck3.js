

GetById1("Auth1").onclick = 
function Soz3(){
	// console.log()
  let log1 = GetById1("username").value;
  
  let pass1 = GetById1("password").value;
  
		if ((pass1.length < 8) || (Search1(pass1, " "))) {
			console.log(Boolean(Search1(pass1, " ")));
			GetById1("Enter1").innerHTML = "Ошибка";
			
			GetById1("password").style.borderColor = "red";
			GetById1("Passwarn1").innerHTML = "Пароль должен составлять минимум 8 символов\n"+
			"(Ваша длина: "+ pass1.length +" ). Без содержания пробелов.";
		} else {
			GetById1("password").style.borderColor = "greenyellow";
		}
		if (log1 === ''){
			GetById1("Enter1").innerHTML = "Ошибка";
			GetById1("username").style.borderColor = "red";
			GetById1("Passwarn1").innerHTML = " Введите логин."

		} else {
			GetById1("username").style.borderColor = "greenyellow";
		}
		if (!((pass1.length < 8) || (Search1(pass1, " ")) || log1 === '' )){
		GetById1("password").type = "password";
		GetById1("Vis1").remove();
		GetById1("Enter1").innerHTML = "Вход";
		GetById1("Passwarn1").innerHTML = "";
		GetById1("Auth1").type = "sumbit"
		// GetById1("aform").method="post";
		// GetById1("aform").action="/auth/log";

		}
}

