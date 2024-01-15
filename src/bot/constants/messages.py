START_MESSAGE = (
    "Привет 👋 \n"
    'Здесь ты можешь поиграть с друзьями в аналог игры "Бункер"\n'
    "Приглашай их сюда, создавай комнату и я сгенерирую вам случайную "
    "партию игры.\nЕсли хочешь узнать подробности как это "
    "сделать напиши /help\n"
    "А если хочешь узнать правила игры напиши /rules"
)
HELP_MESSAGE = (
    "1. Чтобы создать комнату для игры напиши /new_room - "
    "после этого я тебе скажу номер твоей комнаты. Скажи этот номер "
    "своим друзьям и они зайдут к тебе\n"
    "2. Чтобы зайти в комнату напиши /enter_room - после этого напиши "
    "номер комнаты и жди пока администратор комнаты запустит игру\n"
    "3. Если ты администратор комнаты ты можешь управлять ей "
    "(выгонять игроков, начинать игру) с помощью специальных кнопок\n"
    "4. Если ты хочешь посмотреть информацию о своей комнате напиши /my_room\n"
    "5. Если ты хочешь выйти из комнаты напиши /leave_room"
)
RULES_MESSAGE = (
    "По легенде, на земле произошла катастрофа. "
    "Единственный способ спастись — бункер, "
    "куда берут далеко не всех. Игра развивает "
    "дискуссионные навыки, помогает находить "
    "нужные аргументы.\n\n"
    "Игроки — это немногие выжившие после "
    "обрушившейся на планету катастрофы. "
    "Цель каждого из них — попасть в бункер, "
    "ведь там места хватит только для половины. "
    "Команда, в свою очередь, должна следить, "
    "чтобы в укрытии оказался только здоровый генофонд."
)
RULES_MESSAGE_2 = (
    "Сначала все участники игры обезличены. Каждый получает по одной "
    "случайной характеристике из категорий: "
    "профессия; "
    "здоровье; "
    "биологические характеристики; "
    "хобби; "
    "фобии; "
    "дополнительная информация; "
    "человеческие качества. "
    "Помимо того, выдаются по 2 специальных действия "
    "Первой вскрывают карту «Профессия». Например, первый игрок "
    "озвучивает, что он является разносчиком пиццы. "
    "На следующем этапе игроки сами решают, какую из 6 карт, "
    "помимо «Специальных условий», они хотят открыть другим игрокам. "
    "После защиты по двум картам игроки должны выбрать кандидата, "
    "который останется в лесу. Мнение высказывают в "
    "одном круге по часовой стрелке, в следующем — против. "
    "Участники открывают следующую карту. История сохраненного в "
    "игре разносчика пиццы может продолжиться картой «Хобби» — "
    "«Изучение топографических карт»: "
    "Озвучивается четвертая карта. Пусть это будет "
    "«Дополнительные условия» — «Умение ориентироваться по звездам». "
    "Далее снова проводится голосование против одного из участников игры. "
    "Далее озвучивается оставшиеся карты и проводится голосование до тех "
    "пор пока не останется допустимое количество людей в бункере "
    "В конце игры участники, которые не дошли до финиша, "
    "открывают свои карты. Далее всей компанией оценивают, "
    "правильно ли был сделан выбор в каждом круге."
)
CREATE_ROOM_MESSAGE = "Комната успешно создана!\n" "Номер комнаты: {}"
NOT_CREATED_ROOM_MESSAGE = (
    "Ты уже находишься в комнате №{} и не можешь создать новую!"
)
USER_CANT_ENTER_ROOM = (
    "Ты уже находишься в комнате №{}! Для начала выйди из текущей комнаты."
)
ENTER_ROOM_SLUG_MESSAGE = "Введи номер комнаты."
NO_ROOM_MESSAGE = "Комнаты с таким номером не существует!"
ROOM_STARTED_MESSAGE = "В данной комнате игра уже стартовала!"
USER_ENTERED_ROOM_MESSAGE = "Ты успешно зашел в комнату!"
USER_ENTERED_ROOM_ADMIN_MESSAGE = "{} зашел в комнату."
USER_LEAVE_ROOM_MESSAGE = "Ты вышел из комнаты."
CHARACTER_GET_MESSAGE = (
    "Профессия 🎓: <b>{}</b>\n"
    "Био характеристики 🧑‍🦲: <b>{} {} лет/года ({})</b>\n"
    "Состояние здоровья 🏥: <b>{}</b>\n"
    "Фобия 🕷: <b>{}</b>\n"
    "Хобби 🎯: <b>{}</b>\n"
    "Характер 😈: <b>{}</b>\n"
    "Доп. Информация ℹ️: <b>{}</b>\n"
    "Багаж 👝: <b>{}</b>\n"
    "<b>Карты действия ↗️:</b>\n"
    "1️⃣ <b>{}</b>\n"
    "2️⃣ <b>{}</b>"
)
EPIDEMIA_GET_MESSAGE = (
    "В мире произошло 🌋: <b>{}</b>\n"
    "До выхода на поверхность ⌛️: <b>{} лет(года)</b>"
)
BUNKER_GET_MESSAGE = (
    "Бункер: <b>{}</b>\n"
    "Количество мест в бункере: <b>{}</b>\n"
    "<b>Комнаты:</b>\n"
    "1️⃣ <b>{}</b>\n"
    "2️⃣ <b>{}</b>\n"
    "3️⃣ <b>{}</b>"
)
NOT_ENOUGH_PLAYERS_MESSAGE = (
    "Для начала игры требуется как минимум {} игрока(ов)."
)
GAME_STARTED_MESSAGE = (
    "Игра началась! Изучи своего персонажа и произошедшую катастрофу. Удачи"
)
ROOM_IS_CLOSED_MESSAGE = "Ваша комната была закрыта администратором - {}"
PLAYER_LEFT_ROOM_MESSAGE = "{} вышел из комнаты."
ROOM_GET_MESSAGE = "Комната №{}\n" "Количество игроков: {}\n" "{}"
YOU_LEFT_ROOM_MESSAGE = "Ты успешно вышел из комнаты №{}"
KICKED_USER_MESSAGE = "Тебя выгнали из комнаты"
MESSAGE_ABOUT_KICKED_PLAYER = "Администратор комнаты выгнал игрока - {}"
