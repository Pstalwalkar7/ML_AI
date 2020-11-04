
import random
from client_moodle import *
key = 'l3lUMWCLeL6NiyvULfC3FB2KM5oDGNLA1enEZPj3x7556C5xTZ'
trace = open("TRACE.txt","a")

def initialize_population(overfit_array,population_count,variety = None,more_variety = None):
    length = len(overfit_array)
    population = []
    lim = 0
    if variety == None:
        lim = 1
    elif more_variety == None:
        lim = 2
    else:
        lim = 3
    for i in range(population_count):
        chromosome = [0 for i in range(length)]
        for j in range(length):
            rand = random.randrange(0,lim)
            if rand == 0:
                chromosome[j] = overfit_array[j] + random.uniform(-0.6,0.6) * overfit_array[j]
            elif rand == 1:
                chromosome[j] = variety[j] + random.uniform(-0.6,0.6) * variety[j]
            elif rand == 2:
                chromosome[j] = more_variety[j] + random.uniform(-0.6,0.6) * more_variety[j]
            if chromosome[j] > 10.0:
                chromosome[j] = 10.0
            elif chromosome[j] < -10.0:
                chromosome[j] = -10.0
        population.append(chromosome)
    trace.write("INITIAL POPULATION ::"+ str(population)+"\n\n")
    return population

def calculate_net_error(received_error):
    net_error_parameter = received_error[0] + received_error[1] + abs(received_error[0] - received_error[1]) 
    # net_error_parameter = received_error[0] + received_error[1]
    return net_error_parameter

def calculate_fitness(calculated_net_error):
    fitness_parameter = (pow(10,35))/calculated_net_error
    return fitness_parameter

def crossover(parent_1,parent_2):
    # uniform method
    trace.write("Parent 1:\n"+str(parent_1)+"\n")
    trace.write("Parent 2:\n"+str(parent_2)+"\n")
    child = [0 for i in range(len(parent_1))]
    for i in range(len(parent_1)):
        choose = random.randint(0,1)
        if choose == 0:
            child[i] = parent_1[i]
        else:
            child[i] = parent_2[i]
    trace.write("Forms child:"+str(child)+"\n")
    return child

def mutate(child,mutate_parameter):
    trace.write("Child mutates from : \n"+str(child)+"\n")
    change_flag = False
    mutate_above = 1 - mutate_parameter
    random_number = random.uniform(-0.5,0.5)
    if random_number > mutate_above:
        change_flag = True
        changing_indices = []
        changing_number = random.randint(7,11)
        for i in range(changing_number):
            changing_index = random.randint(0,10)
            while changing_index in changing_indices:
                changing_index = random.randint(0,10)
        for X in changing_indices:
            random_number = random.uniform(-1,1)
            child[X] = child[X] + random_number * child[X]
            if child[X] > 10:
                child[X] = 10
            elif child[X] <-10:
                child[X] = -10
    trace.write("To:\n"+str(child)+"\n")
    trace.write("Child has changed?"+str(change_flag)+"\n")
        
def condition_evaluator(condition_parameter):    # to be changed..
    return True

def fill_details(population):
    Details = []
    for chromosome in population:
        received_error = get_errors(key,chromosome)
        net_error = calculate_net_error(received_error)
        fitness = calculate_fitness(net_error)
        detail = [chromosome, received_error, fitness]
        Details.append(detail)
    return Details

## NOT USING THE FOLLOWING 2 Functions 
def generate_cumulative_fitness_array(fitness_array):
    length = len(fitness_array)
    cumulative_fitness_array = [0 for i in range(length)]
    cumulative_fitness_array[0] = fitness_array[0]
    for i in range(1,length):
        cumulative_fitness_array[i] = cumulative_fitness_array[i-1] + fitness_array[i]
    return cumulative_fitness_array

def select_by_fitness(cumulative_fitness_array):
    length = len(cumulative_fitness_array)
    random_number = random.uniform(0,cumulative_fitness_array[length - 1])
    lower = 0
    upper = length - 1
    mid = (lower+upper)//2

    while lower<= upper:
        mid = (lower+upper)//2
        if cumulative_fitness_array[mid] < random_number:
            lower = mid + 1
        else:    # obviously, cumulative_fitness_array[mid] >= random_number
            if mid == 0 or cumulative_fitness_array[mid-1] < random_number:
                break   # thats the mid I want
            else:
                upper = mid -1
    return mid 
## End of unusef functions

def generate_next_generation(population, cumulative_fitness_array, mutation_parameter):
    children = []
    init_pop_cnt = len(population)
    for i in range(init_pop_cnt//2):
        chromosome = population[0]
        select_mate = population[random.randint(1,len(population)-1)]
        child = crossover(chromosome,select_mate)
        mutate(child, mutation_parameter)
        population.remove(chromosome)
        population.remove(select_mate)
        children.append(child)
    return children

if __name__ == '__main__':
    population_parameter = 10
    default_mutation_parameter = 0.12
    enhanced_mutation_parameter = 0.3
    mutation_parameter = default_mutation_parameter
    
    overfit = open("overfit.txt","r")
    overfit = overfit.read()
    overfit_array = overfit.strip("][\n").split(",")
    for i in range(len(overfit_array)):
        overfit_array[i] = float(overfit_array[i])

    for i in range(len(overfit_array)):
        overfit_array[i] = 0.8  * overfit_array[i]


    # overfit_array = [0.0, 0.32577345193061813, -0.3177848481868655, 0.008144500596177624, 0.0003013589049388807, 7.42467744344015e-05, -4.870018849297719e-06, -5.107929847035886e-08, 4.685345169139951e-09, 1.2229047804985439e-11, -1.1342897152448557e-12]
    # variety = [0.0, 0.5014326916177565, -0.10457348513573508, 0.007111485215797348, 0.00022154272143752992, 7.805666209318192e-05, -5.65211128522026e-06, -5.520284168289902e-08, 5.5935247445622456e-09, 1.3061972758578108e-11, -1.3741784115234923e-12]
    # more_variety = [0.0, 0.31156891931738795, -0.26734252726518526, 0.0032341938223367354, 0.00023833668999228693, 7.322085327160956e-05, -3.180977922316933e-06, -5.1887048094680624e-08, 3.610564410425134e-09, 1.3270816723650825e-11, -1.0035627592945416e-12]
    parent_population = initialize_population(overfit_array,population_parameter)
    parent_details = fill_details(parent_population)
    iterations = 0
    iterations_parameter = 8
    condition_parameter = True
    last_max = 0
    expected_increment_parameter = 0.08
    output = open("last_few.txt","a")
    output.write("\n\nNEW TRY::\n\n")
    last_time_best_fitness = 0
    this_time_best_fitness = parent_details[0][2]
    while condition_parameter and iterations<= iterations_parameter:  # removing iterations
        print("---------------------ITERATION::",iterations,"---------------")
        output.write("---------------------ITERATION::" + str(iterations)+"---")
        trace.write("\n\nITERATION:"+str(iterations)+"\n\nMutation Factor of :"+str(mutation_parameter)+"\n\n")
        print("LAST:",last_time_best_fitness)
        print("THIS:",this_time_best_fitness)
        print("MUTATION_PARAM",mutation_parameter)
        parent_details = sorted(parent_details,key = lambda  x : x[2],reverse = True)
        print("Fitness:")
        fitness = []
        for i in parent_details:
            fitness.append(i[2])
        print("PARENTS:")
        for i in range(len(parent_details)):
            print(i,"::",parent_details[i][1],"::",parent_details[i][2])
            output.write("----i:"+ str(i)+"\nMutation_param:\n"+str(mutation_parameter)+"----\nChromosome:\n"+str(parent_details[i][0])+"\nErrors:\n"+str(parent_details[i][1])+"\nFitness:\n"+str(parent_details[i][2])+"\n\n")
        input()
        cumulative_fitness_array = generate_cumulative_fitness_array(fitness)
        children_population = generate_next_generation(parent_population, cumulative_fitness_array, mutation_parameter)
        children_details = fill_details(children_population)
        children_details = sorted(children_details,key = lambda  x : x[2],reverse = True)
        print("CHILDREN:")
        for i in range(len(children_details)):
            print(i,"::",children_details[i][1],"::",children_details[i][2])
        input()
        all_details = parent_details + children_details
        all_details = sorted(all_details,key = lambda  x : x[2],reverse = True)
        print("TOGETHER:")
        for i in range(len(all_details)):
            print(i,"::",all_details[i][1],"::",all_details[i][2])
        parent_details = []
        trace.write("FROM:\n"+ str(all_details)+"\n")
        parent_population = []
        for detail_itr in range(population_parameter):
            parent_details.append(all_details[detail_itr])
            parent_population.append(all_details[detail_itr][0])
        trace.write("WE SELECT:\n"+str(parent_details)+"\n")
        last_time_best_fitness = this_time_best_fitness
        this_time_best_fitness = parent_details[0][2]
        if this_time_best_fitness - last_time_best_fitness < expected_increment_parameter * last_time_best_fitness:
            mutation_parameter = enhanced_mutation_parameter
        else:
            mutation_parameter = default_mutation_parameter
        x = input("DONE?")
        iterations += 1
        if x.lower() == "exit":
            break
        elif x.lower() == "y":
              submit(key,parent_details[0][0])
              print("SUbmitteD")        
    submit(key,parent_details[0][0])
    print("SUBMIT")

# TRIED AFTER SEMI- FINAL RUN : RESULT  : NO BETTER THAN BEFORE
# submit(key,[0.0, 0.4593563321558968, -0.26734252726518526, 0.0032341938223367354, 0.00023833668999228693, 7.322085327160956e-05, -3.1222439860523674e-06, -5.1887048094680624e-08, 3.610564410425134e-09, 1.3270816723650825e-11, -1.0035627592945416e-12])
# submit(key,[0.0, 0.4593563321558968, -0.26734252726518526, 0.0032341938223367354, 0.00023833668999228693, 7.322085327160956e-05, -3.180977922316933e-06, -5.1887048094680624e-08, 3.610564410425134e-09, 1.3270816723650825e-11, -1.0035627592945416e-12])
# submit(key,[0.0, 0.32577345193061813, -0.20401170570807353, 0.005707468063673416, 0.00042161152624910203, 7.323160954190987e-05, -3.3950883105702735e-06, -5.652055057574218e-08, 3.065006544659205e-09, 1.52755009216407e-11, -7.372799990305927e-13])
# submit(key,[0.0, 0.31156891931738795, -0.26734252726518526, 0.0026867990636247263, 0.00023833668999228693, 7.322085327160956e-05, -3.180977922316933e-06, -5.1887048094680624e-08, 3.610564410425134e-09, 1.3270816723650825e-11, -1.0035627592945416e-12])


# # THE ANSWER IS HERE::
# submit(key,[0.0, 0.15541556538015364, -0.3119376866383315, 0.0072630284348390054, 0.00021326150001082259, 7.541302877094687e-05, -3.0436288161228857e-06, -5.85348687007503e-08, 2.778055293578732e-09, 1.6007610555041243e-11, -6.355997293418774e-13])  # [475192.6597071417, 267363.67154648795]
# submit(key,[0.0, 0.15541556538015364, -0.3015881058724484, 0.0072630284348390054, 0.00021326150001082259, 7.541302877094687e-05, -3.0436288161228857e-06, -5.85348687007503e-08, 2.778055293578732e-09, 1.6007610555041243e-11, -6.355997293418774e-13]) # [475299.3601965642, 266761.9261294404]
# submit(key,[0.0, 0.15541556538015364, -0.21498810618966627, 0.00974701143971383, 0.0001029200774793757, 7.541302877094687e-05, -3.0436288161228857e-06, -5.85348687007503e-08, 2.778055293578732e-09, 1.6007610555041243e-11, -6.355997293418774e-13]) #[486875.9922647692, 355928.86546435475]
# submit(key,[0.0, 0.15541556538015364, -0.3119376866383315, 0.00974701143971383, 0.00021326150001082259, 7.541302877094687e-05, -3.0436288161228857e-06, -5.85348687007503e-08, 2.778055293578732e-09, 1.6007610555041243e-11, -6.355997293418774e-13]) #[529622.6848532383, 335040.4983540034]
# submit(key,[0.0, 0.15541556538015364, -0.3015881058724484, 0.00974701143971383, 0.00017876013395434138, 7.541302877094687e-05, -3.0436288161228857e-06, -5.85348687007503e-08, 2.778055293578732e-09, 1.4829736366383614e-11, -6.355997293418774e-13])  # [557510.7416511567, 323411.0673851022]

