let nation_chosen
let activity_array

$(function () {
    function c() {
        add_weekdays();
        let array_days = get_array_days();
        let r = 0;
        let u = false;
        // .empty to remove all child elements of of "calendar_content"
        calendar_content.empty();
        while (!u) {
            // Checks for the first place to put a day on the calendar
            if (days_of_week[r] === array_days[0].weekday) {
                u = true
            } else {
                calendar_content.append('<div class="blank"></div>');
                r++
            }
        }
        for (let c = 0; c < 42 - r; c++) {
            if (c >= array_days.length) {
                calendar_content.append('<div class="blank"></div>')
            } else {
                let v = array_days[c].day;
                let m = check_if_today(new Date(year, month - 1, v)) ? `<div id=${v} class="today">` : `<div id=${v}>`;
                calendar_content.append(m + "" + v + "</div>")
            }
        }
        let y = colors[month - 1];
        calendar_header.css("background-color", y).find("h1").text(months[month - 1] + " " + year);
        calendar_weekdays.find("div").css("color", y);
        // calendar_content.find(".today").css("background-color", y);
        size_elements()
    }

    function get_array_days() {
        let e = [];
        for (let r = 1; r < days_in_month(year, month) + 1; r++) {
            e.push({
                day: r,
                weekday: days_of_week[day_of_the_week_number(year, month, r)]
            })
        }
        return e
    }

    function add_weekdays() {
        calendar_weekdays.empty();
        for (let e = 0; e < 7; e++) {
            calendar_weekdays.append("<div>" + days_of_week[e].substring(0, 3) + "</div>")
        }
    }

    function size_elements() {
        let t;
        let n = $("#calendar").css("width", size + "px");
        n.find(t = "#calendar_weekdays, #calendar_content").css("width", size + "px").find("div").css({
            width: size / 7 + "px",
            height: size / 7 + "px",
            "line-height": size / 7 + "px"
        });
        n.find("#calendar_header").css({
            height: size * (1 / 7) + "px"
        }).find('i[class^="icon-chevron"]').css("line-height", size * (1 / 7) + "px")
    }

    function days_in_month(year, month) {
        return (new Date(year, month, 0)).getDate()
    }

    function day_of_the_week_number(year, month, day) {
        return (new Date(year, month - 1, day)).getDay()
    }

    function check_if_today(e) {
        return y(new Date) === y(e)
    }

    function y(e) {
        return e.getFullYear() + "/" + (e.getMonth() + 1) + "/" + e.getDate()
    }

    function get_today_date() {
        let date = new Date;
        year = date.getFullYear();
        month = date.getMonth() + 1
    }

    let size = 480;
    let year
    let month
    let months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"];
    let days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let colors = ["#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800", "#830800"];
    let calendar_element = $("#calendar");
    let calendar_header = calendar_element.find("#calendar_header");
    let calendar_weekdays = calendar_element.find("#calendar_weekdays");
    let calendar_content = calendar_element.find("#calendar_content");
    get_today_date();
    c();
    calendar_header.find('i[class^="icon-chevron"]').on("click", function () {
        let e = $(this);
        let r = function (e) {
            month = e === "next" ? month + 1 : month - 1;
            if (month < 1) {
                month = 12;
                year--
            } else if (month > 12) {
                month = 1;
                year++
            }
            c()
        };
        if (e.attr("class").indexOf("left") !== -1) {
            r("previous")
        } else {
            r("next")
        }
        if (activity_array !== undefined) {
            apply_activity_data()
        }
    })

    function apply_activity_data() {
        let active_type
        if (activity_array[year] !== undefined) {
            if (activity_array[year][month] !== undefined) {
                for (const [key, value] of Object.entries(activity_array[year][month])) {
                    if (value === 1) {
                        active_type = "active_1"
                    } else if (value <= 3) {
                        active_type = "active_2"
                    } else {
                        active_type = "active_3"
                    }
                    $(`#${key}`).toggleClass(active_type);
                }
            }
        }
    }

    function get_and_apply_activity_data(nationid) {
        fetch(`/activity/?nationid=${nationid}`, {
            method: 'GET'
        })
            .then(r => r.json())
            .then(data => {
                activity_array = data["GET"]["activity"]
                apply_activity_data()
            })
    }

    $('#id_nation').on('select2:select', function (e) {
        nation_chosen = e.params.data['id']
        c()
        get_and_apply_activity_data(nation_chosen);
    });

    $('.bi-question-circle').on('click', function () {
        let legend_element = $('.legend')
        if (legend_element.css('visibility') === 'hidden')
            legend_element.css('visibility', 'visible')
        else
            legend_element.css('visibility', 'hidden')
    })
})