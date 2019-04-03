CALC = {
    "f1": "(params.get('qm') * 100) / ((params.get('pv') * params.get('percent')) + (params.get('pn') * (100 - params.get('percent'))))",
    "f2": "params.get('qzh') * params.get('pn')*( (100 - params.get('percent')) / 100)",
    "f2.1": "(params.get('qzh') * params.get('pn')*( (100 - params.get('percent')) / 100)) / params.get('pn')",
    "f3": "(math.pi * math.pow(((params.get('D') - 2 * params.get('H')) / 2000), 2) * params.get('nst') * 1440) / params.get('qecn')",
    "f4": "math.pi * params.get('nsp') * (math.pow((params.get('dvn') / 2000),2) - math.pow(params.get('D') / 2000, 2) - params.get('skpbp'))",
    "f5": "math.pi * math.pow((params.get('D') - 2 * params.get('H')) / 2000, 2) * params.get('hnkt')",
    "f6.1": "(params.get('uped') + (math.sqrt(3) * params.get('iped') * params.get('cosfi') * (params.get('lkl') / params.get('szh')) * params.get('p') * (1 + 0.0043 * (params.get('tpl') - 20)))) * (380 / params.get('uvh'))",
    "f6.2": "( 380 / (params.get('uvh') - 20) ) * ( params.get('fb') / 50) * params.get('uped') * params.get('kf') + (math.sqrt(3) * params.get('iped') * params.get('cosfi') * (params.get('lkl') / params.get('szh')) * params.get('p') * (1 + 0.0043 * (params.get('tpl') - 20)))",
    "f7": "params.get('qzh') - (params.get('nd2') - params.get('nd1')) * math.pi * (math.pow(params.get('dvn') / 2000, 2) - math.pow(params.get('D') / 2000, 2) - params.get('skpbp')) * 1440/params.get('t')",
    "f8": "(params.get('nst2') - params.get('nst1')) * math.pi * (math.pow(params.get('dvn') / 2000, 2) - math.pow(params.get('D') / 2000, 2) - params.get('skpbp')) * 1440/params.get('t')",
    "f8.1": "((params.get('nst2') - params.get('nst1')) * math.pi * (math.pow(params.get('dvn') / 2000, 2) - math.pow(params.get('D') / 2000, 2) - params.get('skpbp')) * 1440/params.get('t') - math.pi *  math.pow((params.get('D') - 2 * params.get('H'))/2000, 2) * params.get('nst2')) * 1440 / params.get('t')",
    "f9": "params.get('nsp') - (((params.get('rd') - params.get('rz')) * 100) / (params.get('pn') * params.get('g')))",
    "f10.1": "params.get('qezn') * params.get('f') / 50",
    "f10.2": "params.get('nezn') * math.pow(params.get('f') / 50, 2)",
    "f10.3": "params.get('qezn') * math.pow(params.get('f') / 50, 3)",
    "f11": "params.get('wd') * (params.get('f') / 50)",
    "f12.1": "(params.get('qzh') * params.get('t1') ) / (params.get('t1') - params.get('t2'))",
    "f12.2": "(params.get('qzh') * (params.get('t1') - params.get('t3') ) ) / (params.get('t1') - params.get('t2'))",
    "f13": "( math.pow(params.get('dvnek') / 2000,2) - math.pow(params.get('dped') / 2000,2) * math.pi * 86400 * math.pow(params.get('irab') / params.get('inom'),2) )",
    "f14": "50 * math.sqrt((40 * params.get('g') + params.get('ndin')) / params.get('nezn'))",
    "f15": "(params.get('qpr') * params.get('tz'))/params.get('qezn')",
    "f15.1": "params.get('tz') - (params.get('qpr') * params.get('tz'))/params.get('qezn')",
    "f16": "params.get('ktmpn') * params.get('iped') * (params.get('uotp') / 1000)",
    "f17": "params.get('ksu') * (380/params.get('uvh')) * params.get('iped') * (params.get('uotp')/1000)",
    "f18": "params.get('tpr') / (60 * params.get('fshag'))",
    "f18.1": "params.get('fshag') * 86400 / params.get('tpr')",
    "f19": "((params.get('nvd') - params.get('udl') ) * params.get('g') * params.get('pzh') + params.get('rizb') ) * params.get('k') / ((params.get('nvd') - params.get('udl')) * params.get('g'))",
    "f20.1": "(params.get('pezn') * params.get('tezn')) / (24 * params.get('qzh'))",
    "f20.2": "(math.sqrt(3) * params.get('uotp') * params.get('uvh') * params.get('irab') * params.get('cosfi') * params.get('tezn')) / (1000 * 380 * 24 * params.get('qzh'))",
    "f21": "(params.get('zagr') * params.get('iped') * 0.85 ) / (params.get('irab') * 100)",
    "f22": "2 * round(math.degrees(math.asin( (40 * params.get('s')) / (4 * math.pow(params.get('s'), 2) + math.pow(params.get('l'), 2)) ),2 ))"

}
FORMULAS = {
    "f1": {
        "input": [
            {
                "title": "дебит жидкости",
                "symbol": "Qm",
                "name": "qm",
                "dimension": "т/сут"
            },
            {
                "title": "плотность нефти",
                "symbol": "ρ(н)",
                "name": "pn",
                "dimension": "г/см3"
            },
            {
                "title": "обводнённость продукции",
                "symbol": "%",
                "name": "percent",
                "dimension": "%"
            }
        ],
        "constant": [
            {
                "title": "плотность воды",
                "symbol": "ρ(в)",
                "name": "pv",
                "dimension": "г/см3",
                "value": 1.01
            }
        ],
        "output": [
            {
                "title": "дебит жидкости",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут",
                "formula": "f1"
            }
        ],
    },
    "f2": {
        "input": [
            {
                "title": "дебит жидкости",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "плотность нефти",
                "symbol": "ρ(н)",
                "name": "pn",
                "dimension": "г/см3"
            },
            {
                "title": "обводнённость продукции",
                "symbol": "%",
                "name": "percent",
                "dimension": "%"
            }
        ],
        "constant": [
            {
                "title": "плотность воды",
                "symbol": "ρ(в)",
                "name": "pv",
                "dimension": "г/см3",
                "value": 1.01
            }
        ],
        "output": [
            {
                "title": "дебит нефти",
                "symbol": "Qнт",
                "dimension": "т/сут",
                "name": "qnt",
                "formula": "f2"

            },
            {
                "title": "объемный дебит нефти",
                "symbol": "Qнv",
                "name": "qnv",
                "dimension": "м3/сут",
                "formula": "f2.1"
            }
        ],
    },
    "f3": {
        "input": [
            {
                "title": "производительность ЭЦН",
                "symbol": "Qэцн",
                "name": "qecn",
                "dimension": "м3/сут"
            },
            {
                "title": "статический уровень в НКТ",
                "symbol": "Нст(нкт)",
                "name": "nst",
                "dimension": "м"
            },
            {
                "title": "внешний диаметр и толщина стенки",
                "symbol": "Тип НКТ",
                "name": "nkt",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '60x5',
                        'value': '60x5'
                    },
                    {
                        'name': '73x5.5',
                        'value': '73x5.5'
                    },
                    {
                        'name': '73x7',
                        'value': '73x7'
                    },
                    {
                        'name': '89x6.5',
                        'value': '89x6.5'
                    },
                    {
                        'name': '89x8',
                        'value': '89x8'
                    }
                ],
            }
        ],
        "output": [
            {
                "title": "время до появления подачи",
                "symbol": "T",
                "dimension": "мин",
                "name": "T",
                "formula": "f3"

            }
        ],
    },
    "f4": {
        "input": [
            {
                "title": "внутренний диаметр эксплуатационной колонны",
                "symbol": "Dвн.эк",
                "name": "dvn",
                "dimension": "мм"
            },
            {
                "title": "глубина спуска",
                "symbol": "Нсп",
                "name": "nsp",
                "dimension": "м"
            },
            {
                "title": "внешний диаметр и толщина стенки",
                "symbol": "Тип НКТ",
                "name": "nkt",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '60x5',
                        'value': '60x5'
                    },
                    {
                        'name': '73x5.5',
                        'value': '73x5.5'
                    },
                    {
                        'name': '73x7',
                        'value': '73x7'
                    },
                    {
                        'name': '89x6.5',
                        'value': '89x6.5'
                    },
                    {
                        'name': '89x8',
                        'value': '89x8'
                    }
                ],
            }
        ],
        "constant": [
            {
                "title": "площадь сечения кабеля КПБП, 3*16 (15х37мм)",
                "symbol": "Sкпбп",
                "name": "skpbp",
                "dimension": "м2",
                "value": 0.0005066
            }
        ],
        "output": [
            {
                "title": "объем затрубного кольцевого пространства",
                "symbol": "V",
                "dimension": "м3",
                "name": "V",
                "formula": "f4"

            }
        ],
    },
    "f5": {
        "input": [
            {
                "title": "длина подвески",
                "symbol": "Hнкт",
                "name": "hnkt",
                "dimension": "м"
            },
            {
                "title": "внешний диаметр и толщина стенки",
                "symbol": "Тип НКТ",
                "name": "nkt",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '60x5',
                        'value': '60x5'
                    },
                    {
                        'name': '73x5.5',
                        'value': '73x5.5'
                    },
                    {
                        'name': '73x7',
                        'value': '73x7'
                    },
                    {
                        'name': '89x6.5',
                        'value': '89x6.5'
                    },
                    {
                        'name': '89x8',
                        'value': '89x8'
                    }
                ],
            }
        ],
        "output": [
            {
                "title": "внутренний объем колонны НКТ",
                "symbol": "Vнкт",
                "dimension": "м3",
                "name": "vnkt",
                "formula": "f5"

            }
        ],
    },
    "f6.1": {
        "input": [
            {
                "title": "напряжение питающей сети",
                "symbol": "Uвх",
                "name": "uvh",
                "dimension": "B"
            },
            {
                "title": "номинальное напряжение ПЭД по паспорту",
                "symbol": "Uпэд",
                "name": "uped",
                "dimension": "B",
            },
            {
                "title": "наличие выходного фильтра",
                "symbol": "Входной фильтр",
                "name": "kf",
                "dimension": "",
                "menu": [
                    {
                        'name': 'Да',
                        'value': 1.08
                    },
                    {
                        'name': 'Нет',
                        'value': 1.00
                    }
                ]
            },
            {
                "title": "расчетная частота ПЭД",
                "symbol": "Fр",
                "name": "fp",
                "dimension": "Гц",
            },
            {
                "title": "базовая частота ПЭД",
                "symbol": "Fб",
                "name": "fb",
                "dimension": "Гц",
            },
            {
                "title": "cечение жилы кабеля",
                "symbol": "Sж",
                "name": "szh",
                "dimension": "мм2",
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А",
            },
            {
                "title": "длина кабельной линии",
                "symbol": "Lкл",
                "name": "lkl",
                "dimension": "м",
            },
            {
                "title": "номинальный коэффициент мощности электродвигателя",
                "symbol": "cos(φ)",
                "name": "cosfi",
                "dimension": "",
                "menu": [
                    {
                        'name': 'асинхронный ПЭД',
                        'value': 0.85
                    },
                    {
                        'name': 'вентильный ПЭД',
                        'value': 0.95
                    }
                ],
            },
            {
                "title": "удельное сопротивление проводника",
                "symbol": "ρ",
                "name": "p",
                "dimension": "Ом*мм²/м",
                "menu": [
                    {
                        'name': 'Медь',
                        'value': 0.017
                    },
                    {
                        'name': 'Алюминий',
                        'value': 0.026
                    }
                ],
            },
            {
                "title": "температура пласта",
                "symbol": "Tпл",
                "name": "tpl",
                "dimension": "",
            },
        ],
        "output": [
            {
                "title": "необходимое напряжение отпайки",
                "symbol": "Uотп",
                "dimension": "В",
                "name": "uotp",
                "formula": "f6.1"

            }
        ],
    },
    "f6.2": {
        "input": [
            {
                "title": "напряжение питающей сети",
                "symbol": "Uвх",
                "name": "uvh",
                "dimension": "B"
            },
            {
                "title": "номинальное напряжение ПЭД по паспорту",
                "symbol": "Uпэд",
                "name": "uped",
                "dimension": "B",
            },
            {
                "title": "наличие выходного фильтра",
                "symbol": "Входной фильтр",
                "name": "kf",
                "dimension": "",
                "menu": [
                    {
                        'name': 'Да',
                        'value': 1.08
                    },
                    {
                        'name': 'Нет',
                        'value': 1.00
                    }
                ]
            },
            {
                "title": "расчетная частота ПЭД",
                "symbol": "Fр",
                "name": "fp",
                "dimension": "Гц",
            },
            {
                "title": "базовая частота ПЭД",
                "symbol": "Fб",
                "name": "fb",
                "dimension": "Гц",
            },
            {
                "title": "cечение жилы кабеля",
                "symbol": "Sж",
                "name": "szh",
                "dimension": "мм2",
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А",
            },
            {
                "title": "длина кабельной линии",
                "symbol": "Lкл",
                "name": "lkl",
                "dimension": "м",
            },
            {
                "title": "номинальный коэффициент мощности электродвигателя",
                "symbol": "cos(φ)",
                "name": "cosfi",
                "dimension": "",
                "menu": [
                    {
                        'name': 'асинхронный ПЭД',
                        'value': 0.85
                    },
                    {
                        'name': 'вентильный ПЭД',
                        'value': 0.95
                    }
                ],
            },
            {
                "title": "удельное сопротивление проводника",
                "symbol": "ρ",
                "name": "p",
                "dimension": "Ом*мм²/м",
                "menu": [
                    {
                        'name': 'Медь',
                        'value': 0.017
                    },
                    {
                        'name': 'Алюминий',
                        'value': 0.026
                    }
                ],
            },
            {
                "title": "температура пласта",
                "symbol": "Tпл",
                "name": "tpl",
                "dimension": "",
            },
        ],
        "output": [
            {
                "title": "необходимое напряжение отпайки",
                "symbol": "Uотп",
                "dimension": "В",
                "name": "uotp",
                "formula": "f6.2"

            }
        ],
    },
    "f7": {
        "input": [
            {
                "title": "замер дебита",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "начальный динамический уровень",
                "symbol": "Нд1",
                "name": "nd1",
                "dimension": "м"
            },
            {
                "title": "конечный динамический уровень",
                "symbol": "Нд2",
                "name": "nd2",
                "dimension": "м"
            },
            {
                "title": "время исследования (откачки)",
                "symbol": "T",
                "name": "t",
                "dimension": "мин"
            },
            {
                "title": "внутренний диаметр эксплуатационной колонны",
                "symbol": "Dвн.эк",
                "name": "dvn",
                "dimension": "мин"
            },
            {
                "title": "внешний диаметр и толщина стенки",
                "symbol": "Тип НКТ",
                "name": "nkt",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '60x5',
                        'value': '60x5'
                    },
                    {
                        'name': '73x5.5',
                        'value': '73x5.5'
                    },
                    {
                        'name': '73x7',
                        'value': '73x7'
                    },
                    {
                        'name': '89x6.5',
                        'value': '89x6.5'
                    },
                    {
                        'name': '89x8',
                        'value': '89x8'
                    }
                ],
            }
        ],
        "constant": [
            {
                "title": "площадь сечения кабеля КПБП, 3*16 (15х37мм)",
                "symbol": "Sкпбп",
                "name": "skpbp",
                "dimension": "м2",
                "value": 0.0005066
            }
        ],
        "output": [
            {
                "title": "приток жидкости по откачке",
                "symbol": "Qпр",
                "dimension": "м3/сут",
                "name": "qpr",
                "formula": "f7"

            }
        ],
    },
    "f8": {
        "input": [
            {
                "title": "начальный статический уровень",
                "symbol": "Нст1",
                "name": "nst1",
                "dimension": "м"
            },
            {
                "title": "конечный статический уровень",
                "symbol": "Нст2",
                "name": "nst2",
                "dimension": "м"
            },
            {
                "title": "время исследования (откачки)",
                "symbol": "T",
                "name": "t",
                "dimension": "мин"
            },
            {
                "title": "внутренний диаметр эксплуатационной колонны",
                "symbol": "Dвн.эк",
                "name": "dvn",
                "dimension": "мин"
            },
            {
                "title": "внешний диаметр и толщина стенки",
                "symbol": "Тип НКТ",
                "name": "nkt",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '60x5',
                        'value': '60x5'
                    },
                    {
                        'name': '73x5.5',
                        'value': '73x5.5'
                    },
                    {
                        'name': '73x7',
                        'value': '73x7'
                    },
                    {
                        'name': '89x6.5',
                        'value': '89x6.5'
                    },
                    {
                        'name': '89x8',
                        'value': '89x8'
                    }
                ],
            }
        ],
        "constant": [
            {
                "title": "площадь сечения кабеля КПБП, 3*16 (15х37мм)",
                "symbol": "Sкпбп",
                "name": "skpbp",
                "dimension": "м2",
                "value": 0.0005066
            }
        ],
        "output": [
            {
                "title": "приток жидкости по откачке",
                "symbol": "Qпр при наличии ОК над ЭЦН",
                "dimension": "м3/сут",
                "name": "qpryes",
                "formula": "f8"

            },
            {
                "title": "приток жидкости по откачке",
                "symbol": "Qпр при отсутствии ОК над ЭЦН",
                "dimension": "м3/сут",
                "name": "qprno",
                "formula": "f8.1"

            }
        ],
    },
    "f9": {
        "input": [
            {
                "title": "давление на приёме ЭЦН",
                "symbol": "Pд",
                "name": "rd",
                "dimension": "Атм"
            },
            {
                "title": "затрубное давление",
                "symbol": "Рз",
                "name": "rz",
                "dimension": "Атм"
            },
            {
                "title": "глубина спуска УЭЦН",
                "symbol": "Нсп",
                "name": "nsp",
                "dimension": "м"
            },
            {
                "title": "плотность нефти",
                "symbol": "ρ(н)",
                "name": "pn",
                "dimension": "г/см3"
            }
        ],
        "constant": [
            {
                "title": "ускорение свободного падения",
                "symbol": "g",
                "name": "g",
                "dimension": "м/с2",
                "value": 9.81
            }
        ],
        "output": [
            {
                "title": "уровень жидкости в затрубе по датчику",
                "symbol": "Нд(ст)",
                "dimension": "м",
                "name": "ndst",
                "formula": "f9"
            }
        ],
    },
    "f10": {
        "input": [
            {
                "title": "номинальная производительность ЭЦН",
                "symbol": "Qэцн",
                "name": "qezn",
                "dimension": "м3/сут"
            },
            {
                "title": "номинальный напор ЭЦН",
                "symbol": "Нэцн",
                "name": "nezn",
                "dimension": "м"
            },
            {
                "title": "номинальная потребляемая мощность ЭЦН",
                "symbol": "Wэцн",
                "name": "wezn",
                "dimension": "кВт"
            },
            {
                "title": "расчетная частота",
                "symbol": "F",
                "name": "f",
                "dimension": "Гц"
            }
        ],
        "output": [
            {
                "title": "производительность ЭЦН при расчетной F",
                "symbol": "Q(f)",
                "dimension": "м3/сут",
                "name": "qf",
                "formula": "f10.1"
            },
            {
                "title": "напор ЭЦН при расчетной F",
                "symbol": "Н(f)",
                "dimension": "м",
                "name": "nf",
                "formula": "f10.2"
            },
            {
                "title": "потребляемая мощность ЭЦН при расчетной F",
                "symbol": "W(f)",
                "dimension": "кВт",
                "name": "wf",
                "formula": "f10.3"
            },
        ],
    },
    "f11": {
        "input": [
            {
                "title": "номинальная мощность двигателя",
                "symbol": "Wд",
                "name": "wd",
                "dimension": "кВт"
            },
            {
                "title": "расчетная частота",
                "symbol": "F",
                "name": "f",
                "dimension": "Гц"
            }
        ],
        "output": [
            {
                "title": "мощность двигателя при расчетной F",
                "symbol": "Wд(f)",
                "dimension": "кВт",
                "name": "wdf",
                "formula": "f11"
            }
        ],
    },
    "f12.1": {
        "input": [
            {
                "title": "замер жидкости во время откачки",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "время работы (откачки)",
                "symbol": "T1",
                "name": "t1",
                "dimension": "мин"
            },
            {
                "title": "время восстановления",
                "symbol": "T2",
                "name": "t2",
                "dimension": "мин"
            }
        ],
        "output": [
            {
                "title": "мощность двигателя при расчетной F",
                "symbol": "Wд(f)",
                "dimension": "кВт",
                "name": "wdf",
                "formula": "f12.1"
            }
        ],
    },
    "f12.2": {
        "input": [
            {
                "title": "замер жидкости во время откачки",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "время работы (откачки)",
                "symbol": "T1",
                "name": "t1",
                "dimension": "мин"
            },
            {
                "title": "время восстановления",
                "symbol": "T2",
                "name": "t2",
                "dimension": "мин"
            },
            {
                "title": "время восстановления",
                "symbol": "T3",
                "name": "t3",
                "dimension": "мин"
            },
        ],
        "output": [
            {
                "title": "мощность двигателя при расчетной F",
                "symbol": "Wд(f)",
                "dimension": "кВт",
                "name": "wdf",
                "formula": "f12.2"
            }
        ],
    },
    "f13": {
        "input": [
            {
                "title": "внутренний диаметр эксплуатационной колонны",
                "symbol": "Dвн.эк",
                "name": "dvnek",
                "dimension": "мм"
            },
            {
                "title": "",
                "symbol": "Iном",
                "name": "inom",
                "dimension": "A"
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А"
            },
            {
                "title": "текущее значение тока ПЭД",
                "symbol": "Iраб",
                "name": "irab",
                "dimension": "А"
            },
            {
                "title": "внешний диаметр ПЭД",
                "symbol": "Dпэд",
                "name": "dped",
                "dimension": "мм",
                "menu": [
                    {
                        'name': '103',
                        'value': 103
                    },
                    {
                        'name': '117',
                        'value': 117
                    }
                ]
            },
            {
                "title": "номинальная мощность ПЭД",
                "symbol": "Wпэд",
                "name": "wped",
                "dimension": "кВт",
                "menu": [
                    {'name': '12', 'value': 12}, {'name': ' 16', 'value': 16}, {'name': ' 22', 'value': 22},
                    {'name': ' 28', 'value': 28}, {'name': ' 32', 'value': 32}, {'name': ' 36', 'value': 36},
                    {'name': ' 40', 'value': 40}, {'name': ' 45', 'value': 45}, {'name': ' 50', 'value': 50},
                    {'name': ' 56', 'value': 56}, {'name': ' 63', 'value': 63}, {'name': ' 70', 'value': 70},
                    {'name': ' 80', 'value': 80}, {'name': ' 90', 'value': 90}, {'name': ' 100', 'value': 100},
                    {'name': ' 125', 'value': 125}, {'name': ' 140', 'value': 140}, {'name': ' 150', 'value': 150},
                    {'name': ' 160', 'value': 160}, {'name': ' 180', 'value': 180}, {'name': ' 200', 'value': 200},
                    {'name': ' 220', 'value': 220}, {'name': ' 250', 'value': 250}, {'name': ' 270', 'value': 270},
                    {'name': ' 300', 'value': 300}, {'name': ' 320', 'value': 320}, {'name': ' 360', 'value': 360}
                ]
            },
        ],
        "output": [
            {
                "title": "приток жидкости из пласта",
                "symbol": "Qприт",
                "dimension": "м3/сут",
                "name": "qprit",
                "formula": "f13"
            }
        ],
    },
    "f14": {
        "input": [
            {
                "title": "уровень жидкости в скважине",
                "symbol": "Ндин",
                "name": "ndin",
                "dimension": "м"
            },
            {
                "title": "номинальный напор, развиваемый УЭЦН на частоте 50 Гц (по напорной характеристике УЭЦН)",
                "symbol": "Нэцн",
                "name": "nezn",
                "dimension": "м"
            }
        ],
        "constant": [
            {
                "title": "ускорение свободного падения",
                "symbol": "g",
                "name": "g",
                "dimension": "м/с2",
                "value": 9.81
            }
        ],
        "output": [
            {
                "title": "необходимая частота для опрессовки НКТ до 60Атм",
                "symbol": "F",
                "dimension": "Гц",
                "name": "f",
                "formula": "f14"
            }
        ],
    },
    "f15": {
        "input": [
            {
                "title": "время цикла",
                "symbol": "Тц",
                "name": "tz",
                "dimension": "м"
            },
            {
                "title": "приток жидкости для проектного забойного давления",
                "symbol": "Qпр",
                "name": "qpr",
                "dimension": "м3/сут"
            },
            {
                "title": "расчетная подача спускаемого насоса в рабочий период цикла",
                "symbol": "Qэцн",
                "name": "qezn",
                "dimension": "м3/сут"
            }
        ],
        "output": [
            {
                "title": "время работы",
                "symbol": "Тр",
                "dimension": "мин",
                "name": "tp",
                "formula": "f15"
            },
            {
                "title": "время накопления",
                "symbol": "Тн",
                "dimension": "мин",
                "name": "tn",
                "formula": "f15.1"
            }
        ],
    },
    "f16": {
        "input": [
            {
                "title": "необходимое напряжение отпайки",
                "symbol": "Uотп",
                "name": "uotp",
                "dimension": "В"
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А"
            }
        ],
        "constant": [
            {
                "title": "коэффициент ТМПН",
                "symbol": "Kтмпн",
                "name": "ktmpn",
                "dimension": "",
                "value": 1.786
            }
        ],
        "output": [
            {
                "title": "необходимая мощность ТМПН",
                "symbol": "Wтр",
                "dimension": "кВ*А",
                "name": "wtr",
                "formula": "f16"
            }
        ],
    },
    "f17": {
        "input": [
            {
                "title": "необходимое напряжение отпайки",
                "symbol": "Uотп",
                "name": "uotp",
                "dimension": "В"
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А"
            },
            {
                "title": "напряжение питающей сети",
                "symbol": "Uвх",
                "name": "uvh",
                "dimension": "В"
            }
        ],
        "constant": [
            {
                "title": "коэффициент СУ ",
                "symbol": "Kсу",
                "name": "ksu",
                "dimension": "",
                "value": 2.856
            }
        ],
        "output": [
            {
                "title": "минимальное значение номинального тока СУ (ЧРП)",
                "symbol": "Iсу",
                "dimension": "А",
                "name": "isu",
                "formula": "f17"
            }
        ],
    },
    "f18": {
        "input": [
            {
                "title": "шаг разгона частоты",
                "symbol": "Fшаг",
                "name": "fshag",
                "dimension": "Гц"
            },
            {
                "title": "время разгона по программе",
                "symbol": "Tпр",
                "name": "tpr",
                "dimension": "cек"
            }

        ],
        "output": [
            {
                "title": "время разгона частоты на 1Гц",
                "symbol": "Tгц",
                "dimension": "мин",
                "name": "tgz",
                "formula": "f18"
            },
            {
                "title": "разгон частоты за сутки",
                "symbol": "Fсут",
                "dimension": "Гц",
                "name": "fsut",
                "formula": "f18.1"
            }
        ],
    },
    "f19": {
        "input": [
            {
                "title": "верхние дыры перфорации (кровля пласта)",
                "symbol": "Нвд",
                "name": "nvd",
                "dimension": "В"
            },
            {
                "title": "удлинение на глубине Нвд",
                "symbol": "Удл",
                "name": "udl",
                "dimension": "м"
            },
            {
                "title": "плотность жидкости, находящейся в скважине",
                "symbol": "ρ(ж)",
                "name": "pzh",
                "dimension": "г/см3"
            },
            {
                "title": "замеренное избыточное давление",
                "symbol": "Pизб",
                "name": "rizb",
                "dimension": "Атм"
            },
            {
                "title": "коэффициент запаса",
                "symbol": "К",
                "name": "k",
                "dimension": "",
                "menu": [
                    {
                        'name': '1.00',
                        'value': 1.00
                    },
                    {
                        'name': '1.05',
                        'value': 1.05
                    },
                    {
                        'name': '1.06',
                        'value': 1.06
                    },
                    {
                        'name': '1.07',
                        'value': 1.07
                    },
                    {
                        'name': '1.08',
                        'value': 1.08
                    },
                    {
                        'name': '1.09',
                        'value': 1.09
                    },
                    {
                        'name': '1.1',
                        'value': 1.1
                    },
                ]
            },

        ],
        "constant": [
            {
                "title": "ускорение свободного падения",
                "symbol": "g",
                "name": "g",
                "dimension": "м/с2",
                "value": 9.81
            }
        ],
        "output": [
            {
                "title": "необходимая плотность раствора глушения",
                "symbol": "ρ(гл)",
                "dimension": "г/см3",
                "name": "pgl",
                "formula": "f19"
            }
        ],
    },
    "f20.1": {
        "input": [
            {
                "title": "суточный дебит УЭЦН",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "время отработанное УЭЦН за сутки",
                "symbol": "Tэцн",
                "name": "tezn",
                "dimension": "час"
            },
            {
                "title": "потребляемая мощность УЭЦН",
                "symbol": "Pэцн",
                "name": "pezn",
                "dimension": "кВт/сут"
            }
        ],
        "output": [
            {
                "title": "удельное потребление электроэнергии на добычу 1 м3 жидкости   ",
                "symbol": "ω",
                "dimension": "",
                "name": "w",
                "formula": "f20.1"
            }
        ],
    },
    "f20.2": {
        "input": [
            {
                "title": "суточный дебит УЭЦН",
                "symbol": "Qж",
                "name": "qzh",
                "dimension": "м3/сут"
            },
            {
                "title": "время отработанное УЭЦН за сутки",
                "symbol": "Tэцн",
                "name": "tezn",
                "dimension": "час"
            },
            {
                "title": "напряжение отпайки",
                "symbol": "Uотп",
                "name": "uotp",
                "dimension": "В"
            },
            {
                "title": "напряжение питающей сети",
                "symbol": "Uвх",
                "name": "uvh",
                "dimension": "В"
            },
            {
                "title": "коэффициент мощности",
                "symbol": "cosφ",
                "name": "cosfi",
                "dimension": ""
            },
            {
                "title": "сила тока",
                "symbol": "Iраб",
                "name": "irab",
                "dimension": "А"
            },
        ],
        "output": [
            {
                "title": "удельное потребление электроэнергии на добычу 1 м3 жидкости   ",
                "symbol": "ω",
                "dimension": "",
                "name": "w",
                "formula": "f20.2"
            }
        ],
    },
    "f21": {
        "input": [
            {
                "title": "текущая загрузка",
                "symbol": "Загр.тек",
                "name": "zagr",
                "dimension": "%"
            },
            {
                "title": "номинальный ток ПЭД по паспорту",
                "symbol": "Iпэд",
                "name": "iped",
                "dimension": "А"
            },
            {
                "title": "текущее значение тока ПЭД",
                "symbol": "Iраб",
                "name": "irab",
                "dimension": "А"
            }
        ],
        "output": [
            {
                "title": "коэффициента мощности",
                "symbol": "cosφ",
                "dimension": "",
                "name": "cosfi",
                "formula": "f21"
            }
        ],
    },
    "f22": {
        "input": [
            {
                "title": "длина установки",
                "symbol": "L",
                "name": "l",
                "dimension": "м"
            },
            {
                "title": "зазор между внутренним диаметром обсадной колонны и максимальным габаритом  установки",
                "symbol": "S",
                "name": "s",
                "dimension": "м"
            }
        ],
        "output": [
            {
                "title": "допустимый темп набора кривизны в зоне подвески насоса",
                "symbol": "α",
                "dimension": "градусов/10м",
                "name": "a",
                "formula": "f22"
            }
        ],
    },

}
