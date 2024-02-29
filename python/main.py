from IR5G import *
import simulation_rr as rr
import simulation_hg as hg
import simulation_vg as vg
import numpy as np  

#In the following lines random numbers are being generated for the scale factors value, according to the each VNF predefinition

high = random.randrange(8,11)
moderate = random.randrange(6,8)
low = random.randrange(4,6)
up_video = random.randrange(75,77)
up_voz = random.randrange(46,48)

#Mind that there are three different and independent scenarios with its own computational resources, slices, subscribers and scale factors. 
#However, all of these parameters are similar for a fair comparisson

#The slice instantiation receives the slice object, and the four possible scale factor values, randomly generated previously

#eMBB Video and eMBB Voice respectively instantiated for the round-robbin allocation scenario
slice_video_init(rr.eMBBvideo,up_video,high,moderate,low)
slice_voice_init(rr.eMBBvoice,up_voz,high,moderate,low)

#eMBB Video and eMBB Voice respectively instantiated for the horizontal-greedy allocation scenario
slice_video_init(hg.eMBBvideo,up_video,high,moderate,low)
slice_voice_init(hg.eMBBvoice,up_voz,high,moderate,low)

#eMBB Video and eMBB Voice respectively instantiated for the vertical-greedy allocation scenario
slice_video_init(vg.eMBBvideo,up_video,high,moderate,low)
slice_voice_init(vg.eMBBvoice,up_voz,high,moderate,low)

run = 1 #This value controls the simulation loop.
max_run = 1000 #This value sets the maximum number of iterations

#The vectors below are flags to control 
#Position 0 sets
rr_info = [1,1]
hg_info = [1,1]
vg_info = [1,1]

results_rr = open(f'RR/rr-results.txt', "w")
mapping_rr = open(f'RR/rr-mapping.txt', "w")
results_hg = open(f'HG/hg-results.txt', "w")
mapping_hg = open(f'HG/hg-mapping.txt', "w") 
results_vg = open(f'VG/vg-results.txt', "w")
mapping_vg = open(f'VG/vg-mapping.txt', "w")



while run <= max_run:
    loop_times = 0
    loop = 1
    log_rr = open(f'RR/rr-mapping#run{run}.txt', "w")
    log_hg = open(f'HG/hg-mapping#run{run}.txt', "w")
    log_vg = open(f'VG/vg-mapping#run{run}.txt', "w")
    rr_info[0] = 1
    hg_info[0] = 1
    vg_info[0] = 1
    rr_info[1] = 1
    hg_info[1] = 1
    vg_info[1] = 1
    print(f'Run#{run}')
    while loop:
        #print(rr_info[0] or hg_info[0] or vg_info[0], rr_info[0], hg_info[0], vg_info[0])
        #new_subs = random.random()
        new_subs = np.random.poisson(2500)
        loop_times = loop_times + 1
        if rr_info[0]:
            rr.simulation_add_subscriber(new_subs,results_rr,mapping_rr,log_rr,rr_info)
        if hg_info[0]:
            hg.simulation_add_subscriber(new_subs,results_hg,mapping_hg,log_hg,hg_info)
        if vg_info[0]:
            vg.simulation_add_subscriber(new_subs,results_vg,mapping_vg,log_vg,vg_info)
        loop = rr_info[0] or hg_info[0] or vg_info[0]
    mapping_rr.write("\n")
    mapping_hg.write("\n")
    mapping_vg.write("\n")

    log_rr.close()
    log_hg.close()
    log_vg.close()
    rr.reset_blade(rr.anti_affinity_list)
    hg.reset_blade(hg.anti_affinity_list)
    vg.reset_blade(vg.anti_affinity_list, vg.vgreedy)

    high = random.randrange(8,11)
    moderate = random.randrange(6,8)
    low = random.randrange(4,6)
    up_video = random.randrange(75,77)
    up_voz = random.randrange(46,48)

    slice_video_sf_update(rr.eMBBvideo,up_video,high,moderate,low)
    slice_voice_sf_update(rr.eMBBvoice,up_voz,high,moderate,low)

    slice_video_sf_update(hg.eMBBvideo,up_video,high,moderate,low)
    slice_voice_sf_update(hg.eMBBvoice,up_voz,high,moderate,low)

    slice_video_sf_update(vg.eMBBvideo,up_video,high,moderate,low)
    slice_voice_sf_update(vg.eMBBvoice,up_voz,high,moderate,low)

    run = run+1
