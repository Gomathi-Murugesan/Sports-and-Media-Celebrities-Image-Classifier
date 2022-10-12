Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "/app2/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            /* 
            Below is a sample response if you have two faces in an image lets say ronaldo and roger together.
            Most of the time if there is one person in the image you will get only one element in below array
            data = [
                {
                    class: "cristiano_ronaldo",
                    class_probability: [88.95, 0.78, 3.79, 1.03, 1.47, 1.13, 1.93, 0.93],
                    class_dictionary: {'cristiano_ronaldo': 0,
                                'ellen_pompeo': 1,
                                'hrithik_roshan': 2,
                                'mahendra_singh_dhoni': 3,
                                'megan_boone': 4,
                                'priyanka_chopra': 5,
                                'roger_federer': 6,
                                'trisha_krishnan': 7}
                },
                {
                    class: "roger_federer",
                    class_probability: [7.02, 23.7, 8.00, 6.1, 1.62, 7.89, 82.45, 17.89],
                    class_dictionary: {'cristiano_ronaldo': 0,
                            'ellen_pompeo': 1,
                            'hrithik_roshan': 2,
                            'mahendra_singh_dhoni': 3,
                            'megan_boone': 4,
                            'priyanka_chopra': 5,
                            'roger_federer': 6,
                            'trisha_krishnan': 7}
                }
            ]
            */
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let players = ["cristiano_ronaldo", "ellen_pompeo", "hrithik_roshan", "mahendra_singh_dhoni", "megan_boone", "priyanka_chopra", "roger_federer", "trisha_krishnan"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-player="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let probabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(probabilityScore);
                }
            }
            // dz.removeFile(file);          
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
