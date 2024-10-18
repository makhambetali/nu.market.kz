var langArr = {
    'filters':{
        'ru': 'Фильтры',
        'en': 'Filters'
    },
    'condition': {
        'ru': 'Состояние',
        'en': 'Condition'
    },
    'your-profile': {
        'ru':'Ваш профиль',
        'en':'Your Profile'
    },
    'tekhnika-i-gadzhety': {
        'ru':'Техника и гаджеты',
        'en': 'Tech and gadgets'
    },
    'animals': {
        'ru':'Животные',
        'en': 'Animals'
    },
    'clothe':{
        'ru':'Одежда',
        'en':'Clothe'
    },
    'slaves':{
        'ru':'Рабы',
        'en':'Slaves'
    },
    'new':{
        'ru':'Новые',
        'en': 'New'
    },
    'used':{
        'ru':'Использованные',
        'en':'Used'
    }

}
const translateTo = (chosen_lang) => {
    for(let key in langArr){
        var elem = document.querySelector(`[lang-data="${key}"]`)
        if(elem){
            if(elem.tagName == 'INPUT')
            {
                // alert()
                elem.value = langArr[key][chosen_lang]
            }
            else{
                
                elem.innerHTML = langArr[key][chosen_lang]
            }
        }
        
    }
}
const buttons = document.querySelectorAll(".change_language_button");
buttons.forEach((button) => {
	button.addEventListener("click", () => {
		const language = button.getAttribute("language");
		localStorage.setItem("language", language);
        translateTo(language)
	});
});



document.addEventListener("DOMContentLoaded", () => {
	const savedLanguage = localStorage.getItem("language") || "ru";
    console.log(savedLanguage)
	translateTo(savedLanguage);
});