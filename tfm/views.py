from random import Random
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta, date
from forms import UserRegistrationForm, LoginForm, CreatePatientForm
from tfm.models import Patient
import json


def index(request):
    if request.user.is_authenticated():
        return profile(request)
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Hash the password.
            print form.cleaned_data
            newUser = form.instance
            newUser.password = make_password(newUser.password)
            newUser.email = newUser.username
            newUser.save()
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return HttpResponseRedirect('/profile')
            else:
                print"no"
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def create_patient(request):
    if request.method == 'POST':
        form = CreatePatientForm(request.POST)
        if (form.is_valid()):
            patient = form.instance
            # Since we excluded the sex in the form we need to get in from request.POST.
            patient.sex = request.POST['sex']
            # The patient's doctor is the user
            patient.doctor = request.user
            # Create a date from the form info
            date_string = request.POST['birth_date']
            day = int(date_string[0:2])
            month = int(date_string[3:5])
            year = int(date_string[6:10])
            birth_date = date(year, month, day)
            patient.birth_date = birth_date
            patient.save()
            return HttpResponseRedirect('/patients')
    else:
        form = CreatePatientForm()
    return render(request, 'create_patient.html', {'form': form})


@login_required
def list_patients(request):
    doctor_patients = Patient.objects.filter(doctor=request.user).order_by('last_name')

    for patient in doctor_patients:
        patient.code = str(patient.id).zfill(6)

    return render(request, 'patients.html', {'patients': doctor_patients})


@login_required
def profile(request):
    return render(request, 'profile.html')


def crossdomain(request):
    return HttpResponse(open('crossdomain.xml').read())


def validate_patient_code(request):
    # Take off the zeros to the left.
    code = int(request.GET['code'])
    patient = Patient.objects.filter(id=code)
    response = {}
    if patient:
        response['first_name'] = patient[0].first_name
        response['last_name'] = patient[0].last_name
        response['ok'] = True
    else:
        response['ok'] = False
    print response
    return HttpResponse(json.dumps(response))


def receive_result(request):
    if request.method == 'POST':
        print request.POST['test_type']


def patient(request):
    patient_id = request.GET['id']
    patient_object = Patient.objects.filter(id=patient_id).first()
    patient_object.y = []

    #Sort all the keys
    test_json = json.loads('{"thumb":{"x":{"0":"-53.1064", "1":"-53.29283", "2":"-53.80412", "3":"-54.33689", "4":"-54.53602", "5":"-55.0292", "6":"-55.44897", "7":"-55.74734", "8":"-56.00662", "9":"-56.23918", "10":"-56.30658", "11":"-56.43961", "12":"-56.73438", "13":"-57.22478", "14":"-57.4912", "15":"-57.50881", "16":"-57.49787", "17":"-57.62423", "18":"-57.72678", "19":"-57.59319", "20":"-57.62324", "21":"-57.62021", "22":"-57.42247", "23":"-57.41489", "24":"-57.41489", "25":"-57.06078", "26":"-56.8052", "27":"-56.47527", "28":"-56.23489", "29":"-55.9868", "30":"-55.69312", "31":"-55.63871", "32":"-55.26448", "33":"-55.15112", "34":"-55.05235", "35":"-54.9953", "36":"-54.92916", "37":"-54.75665", "38":"-54.59876", "39":"-54.35603", "40":"-54.28357", "41":"-54.0892", "42":"-53.86315", "43":"-53.89665", "44":"-53.65919", "45":"-53.53048", "46":"-53.25595", "47":"-53.30012", "48":"-53.17508", "49":"-52.98603", "50":"-52.70218", "51":"-52.3926", "52":"-52.24844", "53":"-51.96199", "54":"-51.80866", "55":"-51.8136"}, "y":{"0":"87.11729", "1":"87.67159", "2":"89.93001", "3":"92.70406", "4":"94.20454", "5":"97.34283", "6":"100.414", "7":"103.2348", "8":"106.6868", "9":"110.1455", "10":"112.4721", "11":"116.4494", "12":"121.1863", "13":"125.3603", "14":"129.9948", "15":"133.8486", "16":"135.67", "17":"139.6999", "18":"142.8388", "19":"147.1588", "20":"151.4064", "21":"153.3796", "22":"157.3329", "23":"161.5419", "24":"161.5419", "25":"168.8531", "26":"172.7276", "27":"175.656", "28":"178.2003", "29":"182.0464", "30":"185.3732", "31":"187.1825", "32":"192.1608", "33":"193.7997", "34":"197.0872", "35":"200.6283", "36":"202.7093", "37":"206.205", "38":"209.1807", "39":"211.1638", "40":"211.8564", "41":"213.7761", "42":"214.9394", "43":"216.4708", "44":"217.1687", "45":"217.9778", "46":"217.6859", "47":"217.8811", "48":"217.9968", "49":"217.9218", "50":"217.7347", "51":"217.3666", "52":"217.142", "53":"216.9378", "54":"216.4493", "55":"215.6519"}, "z":{"0":"-95.92974", "1":"-95.231", "2":"-92.23311", "3":"-88.45316", "4":"-86.54145", "5":"-82.24797", "6":"-78.09897", "7":"-74.25504", "8":"-70.64456", "9":"-67.2915", "10":"-65.09949", "11":"-62.17673", "12":"-59.6127", "13":"-57.28981", "14":"-54.82345", "15":"-52.90034", "16":"-51.70015", "17":"-48.80519", "18":"-46.46006", "19":"-43.94049", "20":"-41.1966", "21":"-40.09875", "22":"-37.46537", "23":"-34.4761", "24":"-34.4761", "25":"-30.13964", "26":"-27.44379", "27":"-25.808", "28":"-23.59383", "29":"-20.85704", "30":"-18.63977", "31":"-17.29164", "32":"-14.01197", "33":"-13.10005", "34":"-10.88532", "35":"-8.267746", "36":"-6.808319", "37":"-3.830403", "38":"-1.001923", "39":"1.216102", "40":"1.986003", "41":"5.205736", "42":"8.023695", "43":"11.38125", "44":"14.00907", "45":"17.0717", "46":"19.16232", "47":"20.58471", "48":"23.15759", "49":"25.27142", "50":"27.9376", "51":"29.74997", "52":"30.8802", "53":"33.68273", "54":"35.59508", "55":"36.54762"}}, "index":{"x":{"0":"1.204162", "1":"1.321534", "2":"1.4141", "3":"1.361699", "4":"1.250121", "5":"0.7839159", "6":"0.2748938", "7":"-0.1613522", "8":"-0.6203542", "9":"-0.9006", "10":"-1.008818", "11":"-1.427516", "12":"-2.073366", "13":"-2.715236", "14":"-3.318016", "15":"-3.6389", "16":"-3.729813", "17":"-3.779003", "18":"-3.821148", "19":"-3.928629", "20":"-3.91926", "21":"-3.925122", "22":"-3.871322", "23":"-3.710463", "24":"-3.710463", "25":"-3.492245", "26":"-3.195315", "27":"-3.096152", "28":"-2.912039", "29":"-2.789642", "30":"-2.613829", "31":"-2.494422", "32":"-2.093206", "33":"-2.003056", "34":"-1.973753", "35":"-2.009475", "36":"-2.029003", "37":"-1.589908", "38":"-1.149363", "39":"-0.8120545", "40":"-0.8108531", "41":"-0.5762175", "42":"-0.4557744", "43":"-0.1824435", "44":"0.003745584", "45":"0.25203", "46":"0.2702321", "47":"0.4316477", "48":"0.7503113", "49":"1.100753", "50":"1.724024", "51":"2.280034", "52":"2.579025", "53":"3.160652", "54":"3.242993", "55":"2.908952"}, "y":{"0":"113.7308", "1":"114.4965", "2":"117.8123", "3":"122.1076", "4":"124.3259", "5":"128.5713", "6":"132.4735", "7":"136.1774", "8":"140.1968", "9":"144.1009", "10":"146.7604", "11":"150.9369", "12":"155.6959", "13":"160.4702", "14":"165.3424", "15":"169.4884", "16":"171.7819", "17":"176.4571", "18":"180.7227", "19":"185.4738", "20":"190.0121", "21":"192.0977", "22":"196.2832", "23":"200.4054", "24":"200.4054", "25":"208.6326", "26":"212.8012", "27":"216.1178", "28":"218.9971", "29":"223.1663", "30":"226.6347", "31":"228.5856", "32":"234.3417", "33":"236.2624", "34":"240.0393", "35":"243.8994", "36":"246.3451", "37":"250.116", "38":"253.097", "39":"255.0635", "40":"255.7703", "41":"257.7967", "42":"259.3604", "43":"260.9636", "44":"261.9659", "45":"262.8966", "46":"263.2426", "47":"263.2708", "48":"263.4265", "49":"263.1432", "50":"262.8591", "51":"262.5992", "52":"262.3655", "53":"261.9833", "54":"260.9572", "55":"259.4359"}, "z":{"0":"-30.00513", "1":"-29.69692", "2":"-27.76614", "3":"-25.32685", "4":"-24.07138", "5":"-21.01484", "6":"-17.97012", "7":"-15.15527", "8":"-12.35455", "9":"-9.800903", "10":"-7.98785", "11":"-5.226855", "12":"-2.614871", "13":"-0.9708174", "14":"1.265103", "15":"3.065708", "16":"3.981179", "17":"6.200903", "18":"7.44078", "19":"9.573041", "20":"11.81322", "21":"12.70566", "22":"15.11722", "23":"17.95555", "24":"17.95555", "25":"21.57945", "26":"23.85857", "27":"25.25067", "28":"27.17221", "29":"29.66889", "30":"31.81122", "31":"32.91723", "32":"35.4594", "33":"36.08815", "34":"37.87796", "35":"40.27371", "36":"41.43941", "37":"43.84347", "38":"46.31842", "39":"48.42299", "40":"49.20207", "41":"52.27259", "42":"54.82277", "43":"57.77697", "44":"60.14259", "45":"62.86076", "46":"64.6656", "47":"66.00323", "48":"68.26389", "49":"70.28429", "50":"72.69911", "51":"74.18084", "52":"75.06461", "53":"77.50038", "54":"79.44591", "55":"80.68565"}}, "middle":{"x":{"0":"35.48065", "1":"35.39513", "2":"35.17", "3":"34.71542", "4":"34.468", "5":"33.78359", "6":"33.18582", "7":"32.79689", "8":"32.36207", "9":"32.04488", "10":"31.89002", "11":"31.44672", "12":"30.818", "13":"30.06835", "14":"29.55742", "15":"29.32773", "16":"29.27381", "17":"29.32419", "18":"29.28396", "19":"29.15958", "20":"29.21655", "21":"29.20231", "22":"29.21731", "23":"29.37964", "24":"29.37964", "25":"29.68969", "26":"30.03397", "27":"30.20927", "28":"30.45975", "29":"30.64358", "30":"30.89581", "31":"31.04493", "32":"31.60191", "33":"31.74886", "34":"31.86577", "35":"31.91502", "36":"31.94585", "37":"32.34031", "38":"32.69283", "39":"33.01201", "40":"33.03222", "41":"33.32822", "42":"33.51276", "43":"33.85669", "44":"34.19215", "45":"34.56861", "46":"34.68948", "47":"34.85939", "48":"35.1443", "49":"35.50742", "50":"36.07185", "51":"36.59189", "52":"36.91549", "53":"37.59615", "54":"37.83507", "55":"37.8493"}, "y":{"0":"108.2343", "1":"108.4291", "2":"110.6781", "3":"113.4989", "4":"115.2455", "5":"118.8249", "6":"122.4727", "7":"126.3249", "8":"130.4929", "9":"134.3995", "10":"136.9953", "11":"141.1827", "12":"145.9969", "13":"150.7192", "14":"155.8677", "15":"160.2599", "16":"162.7064", "17":"167.6227", "18":"172.0474", "19":"176.9451", "20":"181.6345", "21":"183.7455", "22":"187.9977", "23":"192.1147", "24":"192.1147", "25":"200.6979", "26":"204.8898", "27":"208.4282", "28":"211.4828", "29":"215.8321", "30":"219.4125", "31":"221.3822", "32":"227.4573", "33":"229.4886", "34":"233.4929", "35":"237.5753", "36":"240.2067", "37":"243.8667", "38":"246.5771", "39":"248.4422", "40":"249.1899", "41":"251.36", "42":"253.1399", "43":"254.6867", "44":"255.8745", "45":"256.9364", "46":"257.4242", "47":"257.3505", "48":"257.1621", "49":"256.8624", "50":"256.1757", "51":"255.5715", "52":"255.2193", "53":"254.6669", "54":"253.4899", "55":"252.6262"}, "z":{"0":"-22.04582", "1":"-21.76156", "2":"-19.92625", "3":"-17.56351", "4":"-16.29338", "5":"-13.21014", "6":"-10.15916", "7":"-7.387317", "8":"-4.624747", "9":"-2.136091", "10":"-0.2752141", "11":"2.549128", "12":"5.257451", "13":"7.339353", "14":"9.579365", "15":"11.32873", "16":"12.25294", "17":"14.31521", "18":"15.58796", "19":"17.68987", "20":"19.75692", "21":"20.62361", "22":"23.01593", "23":"25.7537", "24":"25.7537", "25":"29.30229", "26":"31.52364", "27":"32.88179", "28":"34.72508", "29":"37.1873", "30":"39.27921", "31":"40.32428", "32":"42.72626", "33":"43.31172", "34":"45.01983", "35":"47.35192", "36":"48.46278", "37":"50.81134", "38":"53.30738", "39":"55.4205", "40":"56.20977", "41":"59.15588", "42":"61.61471", "43":"64.45914", "44":"66.67417", "45":"69.22091", "46":"70.97429", "47":"72.2749", "48":"74.55574", "49":"76.43889", "50":"78.81723", "51":"80.25557", "52":"81.03336", "53":"83.26505", "54":"85.04172", "55":"85.8903"}}, "ring":{"x":{"0":"56.60996", "1":"57.13583", "2":"57.28485", "3":"57.30813", "4":"57.2776", "5":"57.03425", "6":"56.71567", "7":"56.48667", "8":"56.0772", "9":"55.71225", "10":"55.59438", "11":"55.25272", "12":"54.58797", "13":"53.86353", "14":"53.26384", "15":"52.85783", "16":"52.73891", "17":"52.61386", "18":"52.46348", "19":"52.29434", "20":"52.23186", "21":"52.21049", "22":"52.29726", "23":"52.39968", "24":"52.39968", "25":"52.68004", "26":"53.00505", "27":"53.1936", "28":"53.43984", "29":"53.61974", "30":"53.85809", "31":"54.00134", "32":"54.5243", "33":"54.64773", "34":"54.75286", "35":"54.78992", "36":"54.77617", "37":"55.0812", "38":"55.40907", "39":"55.71236", "40":"55.70989", "41":"55.93082", "42":"56.02728", "43":"56.15343", "44":"56.44616", "45":"56.73922", "46":"56.89628", "47":"57.03637", "48":"57.29463", "49":"57.61679", "50":"58.15805", "51":"58.71296", "52":"59.01781", "53":"59.68749", "54":"60.02214", "55":"60.05275"}, "y":{"0":"92.88303", "1":"94.1635", "2":"97.22782", "3":"101.4175", "4":"103.6727", "5":"108.2921", "6":"112.6565", "7":"116.997", "8":"121.4357", "9":"125.4896", "10":"128.2039", "11":"132.6801", "12":"137.5408", "13":"141.8905", "14":"147.0678", "15":"151.4232", "16":"153.844", "17":"158.6789", "18":"162.9346", "19":"167.9256", "20":"172.6271", "21":"174.766", "22":"179.2449", "23":"183.3841", "24":"183.3841", "25":"192.0185", "26":"196.2589", "27":"199.9108", "28":"203.0256", "29":"207.4194", "30":"211.0778", "31":"213.0641", "32":"219.2245", "33":"221.2682", "34":"225.3535", "35":"229.496", "36":"232.1737", "37":"235.758", "38":"238.406", "39":"240.2264", "40":"240.917", "41":"242.9594", "42":"244.5156", "43":"245.4399", "44":"246.5533", "45":"247.3369", "46":"247.7195", "47":"247.5112", "48":"247.1891", "49":"246.5672", "50":"245.8824", "51":"245.5182", "52":"245.1309", "53":"244.5102", "54":"243.3882", "55":"242.1794"}, "z":{"0":"-37.3502", "1":"-36.26671", "2":"-34.08944", "3":"-31.45136", "4":"-29.99736", "5":"-26.66073", "6":"-23.38974", "7":"-20.38504", "8":"-17.31949", "9":"-14.66363", "10":"-12.71413", "11":"-9.783034", "12":"-6.861264", "13":"-4.3417", "14":"-1.922285", "15":"-0.02726018", "16":"0.9869974", "17":"3.086307", "18":"4.492502", "19":"6.625097", "20":"8.640299", "21":"9.492596", "22":"11.8105", "23":"14.48404", "24":"14.48404", "25":"18.05058", "26":"20.23296", "27":"21.59593", "28":"23.40969", "29":"25.88556", "30":"27.96576", "31":"28.95897", "32":"31.31797", "33":"31.89963", "34":"33.58059", "35":"35.90408", "36":"37.01641", "37":"39.32329", "38":"41.76162", "39":"43.85479", "40":"44.69784", "41":"47.67538", "42":"50.22905", "43":"53.26841", "44":"55.4775", "45":"58.06673", "46":"59.83073", "47":"61.12838", "48":"63.34875", "49":"65.22857", "50":"67.44428", "51":"68.64896", "52":"69.32692", "53":"71.4043", "54":"73.02581", "55":"73.93255"}}, "pinky":{"x":{"0":"81.48738", "1":"81.24844", "2":"80.8462", "3":"80.42036", "4":"80.2149", "5":"79.64792", "6":"79.10063", "7":"78.75809", "8":"78.35358", "9":"77.92401", "10":"77.75704", "11":"77.42437", "12":"76.8542", "13":"76.09422", "14":"75.57728", "15":"75.28024", "16":"75.18748", "17":"74.97837", "18":"74.7123", "19":"74.48562", "20":"74.28972", "21":"74.19876", "22":"74.25792", "23":"74.34103", "24":"74.34103", "25":"74.60512", "26":"74.83797", "27":"75.00238", "28":"75.21674", "29":"75.38024", "30":"75.61307", "31":"75.69213", "32":"76.12233", "33":"76.20109", "34":"76.25863", "35":"76.28657", "36":"76.27642", "37":"76.53325", "38":"76.8203", "39":"77.12769", "40":"77.17075", "41":"77.43538", "42":"77.67178", "43":"77.85031", "44":"78.14726", "45":"78.41091", "46":"78.65202", "47":"78.74799", "48":"78.9492", "49":"79.22401", "50":"79.63223", "51":"80.0611", "52":"80.27819", "53":"80.7963", "54":"81.07847", "55":"81.18678"}, "y":{"0":"85.15334", "1":"85.75882", "2":"88.1774", "3":"91.69487", "4":"93.58863", "5":"97.62811", "6":"101.6099", "7":"105.7864", "8":"110.2857", "9":"114.4008", "10":"117.013", "11":"121.585", "12":"126.5698", "13":"130.0704", "14":"135.4468", "15":"140.1531", "16":"142.5949", "17":"147.4963", "18":"151.4176", "19":"156.5699", "20":"161.3674", "21":"163.4465", "22":"167.966", "23":"172.1579", "24":"172.1579", "25":"180.7337", "26":"184.8685", "27":"188.5522", "28":"191.6655", "29":"196.03", "30":"199.7424", "31":"201.6821", "32":"207.6628", "33":"209.6361", "34":"213.6669", "35":"217.853", "36":"220.587", "37":"224.0883", "38":"226.6335", "39":"228.4867", "40":"229.2084", "41":"231.4884", "42":"233.6127", "43":"234.8791", "44":"236.2626", "45":"237.243", "46":"238.3907", "47":"238.1429", "48":"237.9665", "49":"237.7544", "50":"237.0923", "51":"236.6139", "52":"236.3725", "53":"235.89", "54":"235.2173", "55":"234.4558"}, "z":{"0":"-59.96474", "1":"-59.88904", "2":"-58.12274", "3":"-55.66757", "4":"-54.23061", "5":"-50.94115", "6":"-47.7889", "7":"-44.96461", "8":"-42.15875", "9":"-39.74379", "10":"-37.81858", "11":"-34.95243", "12":"-32.07912", "13":"-29.15881", "14":"-26.80988", "15":"-25.0483", "16":"-24.04082", "17":"-22.07482", "18":"-20.5928", "19":"-18.50377", "20":"-16.60704", "21":"-15.75747", "22":"-13.48407", "23":"-10.94214", "24":"-10.94214", "25":"-7.395919", "26":"-5.23511", "27":"-3.857806", "28":"-2.072821", "29":"0.4128062", "30":"2.458825", "31":"3.418712", "32":"5.762167", "33":"6.358624", "34":"8.039584", "35":"10.34584", "36":"11.42303", "37":"13.62438", "38":"15.96872", "39":"17.97743", "40":"18.8046", "41":"21.57602", "42":"23.82083", "43":"26.55981", "44":"28.60123", "45":"31.02687", "46":"32.50868", "47":"33.76962", "48":"35.87461", "49":"37.56669", "50":"39.71208", "51":"40.89332", "52":"41.43174", "53":"43.30088", "54":"44.70979", "55":"45.5035"}}, "times":{"0":"0.0165731944143772", "1":"0.0332153830677271", "2":"0.0496991630643606", "3":"0.0662655513733625", "4":"0.0832059942185879", "5":"0.0993986371904612", "6":"0.115965643897653", "7":"0.132532341405749", "8":"0.14922372251749", "9":"0.165665425360203", "10":"0.182232122868299", "11":"0.198798820376396", "12":"0.215365517884493", "13":"0.23193221539259", "14":"0.248498912900686", "15":"0.265099951997399", "16":"0.28163199685514", "17":"0.298199003562331", "18":"0.315208440646529", "19":"0.33133177831769", "20":"0.347899094223976", "21":"0.36470247618854", "22":"0.381202653050423", "23":"0.397599184885621", "24":"0.414171760901809", "25":"0.430731961503625", "26":"0.447299586609006", "27":"0.463865354657173", "28":"0.48043205216527", "29":"0.496999677270651", "30":"0.513705909252167", "31":"0.530205467715859", "32":"0.546714928001165", "33":"0.563265535980463", "34":"0.57983223348856", "35":"0.596398621797562", "36":"0.612965937703848", "37":"0.629532016813755", "38":"0.646098714321852", "39":"0.66270687058568", "40":"0.679232109338045", "41":"0.695799116045237", "42":"0.712368907406926", "43":"0.728967471048236", "44":"0.745703713968396", "45":"0.76223111897707", "46":"0.77863198146224", "47":"0.795198988169432", "48":"0.811769397929311", "49":"0.82833238132298", "50":"0.845227653160691", "51":"0.861466085538268", "52":"0.87803247384727", "53":"0.894599480554461", "54":"0.911171747371554", "55":"0.927734112367034"}}')
    # test_json = json.dumps(test_json, sort_keys=True)

    # Since the fingers and the times aren't sorted it's necessary to do it this way.
    coordinates = ['x', 'y', 'z']
    thumb_coords = [[],[],[]]
    index_coords = [[],[],[]]
    middle_coords = [[],[],[]]
    ring_coords = [[],[],[]]
    pinky_coords = [[],[],[]]
    times = []

    for i in range (0, test_json['times'].keys().__len__()):
        # In each iteration we add either a x, y or z coord.
        for j in range(0, coordinates.__len__()):
            # Add a "[<time>, <position in axis>]," string to each array.
            coordinate = coordinates[j]
            thumb_coords[j].append("[" + test_json['times'][str(i)] + ", " + test_json['thumb'][coordinate][str(i)] + "]")
            index_coords[j].append("[" + test_json['times'][str(i)] + ", " + test_json['index'][coordinate][str(i)] + "]")
            middle_coords[j].append("[" + test_json['times'][str(i)] + ", " + test_json['middle'][coordinate][str(i)] + "]")
            ring_coords[j].append("[" + test_json['times'][str(i)] + ", " + test_json['ring'][coordinate][str(i)] + "]")
            pinky_coords[j].append("[" + test_json['times'][str(i)] + ", " + test_json['pinky'][coordinate][str(i)] + "]")
            if i != test_json['times'].keys().__len__():
                thumb_coords[j].append(",")
                index_coords[j].append(",")
                middle_coords[j].append(",")
                ring_coords[j].append(",")
                pinky_coords[j].append(",")
            # index_coords[j].append(float(test_json['index'][coordinate][str(i)]))
            # middle_coords[j].append(float(test_json['middle'][coordinate][str(i)]))
            # ring_coords[j].append(float(test_json['ring'][coordinate][str(i)]))
            # pinky_coords[j].append(float(test_json['pinky'][coordinate][str(i)]))
        times.append(float(test_json['times'][str(i)]))


    return render(request, 'patient.html', {'patient': patient_object,
                                            'thumb_coords': thumb_coords,
                                            'index_coords': index_coords,
                                            'middle_coords': middle_coords,
                                            'ring_coords': ring_coords,
                                            'pinky_coords': pinky_coords,
                                            'times': times,
                                            })


def send_test_result(request):
    response =  {}
    if request.method == 'POST':
        print request.POST['patient_id']
        response['ok'] = True
    else:
        response['ok'] = False
    return HttpResponse(json.dumps(response))
