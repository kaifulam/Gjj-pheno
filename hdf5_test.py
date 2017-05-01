import numpy as np
import h5py


filepath = '/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/julian/raw_data'

n_samples = 10000000
n_batch = 100000
n_rep = n_samples / n_batch
#tt_split = 0.8    # train test split = 0.8 train, 0.2 test
X_input = []
y_input = []

f = h5py.File(filepath+'/gjj_Variables.hdf5', 'w')
dset_high = f.create_dataset('high_input', (n_samples, 1, 16), maxshape=(None,1,16))
dset_y = f.create_dataset('y_input', (n_samples, 2), maxshape=(None, 2))

#another for loop for n_samples

for k in range(n_rep):
    print 'k = ', k

    X_input = []
    y_input = []
	
    for i in range(n_batch):
        if i % 10000 == 0:
            print '@line number i = ', i

        high = np.load(filepath+'/saved_batches_test/clean_dijet_high_'+str(k*n_batch + i)+'.npy')
		#mid = np.load(filepath+'/saved_batches_test/clean_dijet_mid_'+str(i)+'.npy')
        y = np.load(filepath+'/saved_batches_test/clean_dijet_y_'+str(k*n_batch + i)+'.npy')

        X_input.append(high)

		# y==5 is b jet signal; For y: column 0 background, column 1 signal
        if y == 5:
            y_input.append(np.asarray([0,1]))
        else:
            y_input.append(np.asarray([1,0]))

    #X_input = np.asarray(X_input)
    #y_input = np.asarray(y_input)

    '''# Normalization -- wrong.. should normalize at the very end across all batches...
    for i in range(X_input.shape[2]):
	    var = X_input[:,:,i]
	    var = (var - np.mean(var))/np.std(var)
        X_input[:,:,i] = var'''

    # Set hdf5 dataset
    dset_high[0 + k*n_batch : (1+k) * n_batch, ...] = np.asarray(X_input)
    dset_y[0 + k*n_batch : (1+k) * n_batch, ...] = np.asarray(y_input)

    '''#for de-bugging    
    X_arr, y_arr = np.asarray(X_input), np.asarray(y_input)
    print 'dset_high', dset_high.shape, '\n', dset_high[ 0 + k*n_batch: 0 + k*n_batch + 5, ...]
    print 'X_input', X_arr.shape, '\n', X_arr[0:5, ...]
    print 'dset_y', dset_y.shape, '\n', dset_y[0 + k*n_batch: 0 + k*n_batch + 5, ...]
    print 'y_input', y_arr.shape, '\n', y_arr[0 + k*n_batch: 0 + k*n_batch + 5, ...]'''

