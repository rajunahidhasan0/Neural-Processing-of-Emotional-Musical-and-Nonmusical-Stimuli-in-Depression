library(matlabr)
library(spm12r)
library(neurobase)


if(!have_matlab()){
	stop('404:matlab')
}

add_spm_dir('../spm12')

funcdir <-  'extracted/func/'
anatdir <- 'extracted/anat/'


f <- file('fnames.txt', open='r')
fnames <-readLines(f)

for(fname in fnames){
	file.copy(paste(funcdir, fname, '_func_', fname, '_task-music_run-3_bold.nii', sep=''), 'tmp/')
	functional = paste('tmp/', fname, '_func_', fname, '_task-music_run-3_bold.nii', sep='')
	
	file.copy(paste(anatdir, fname, '_T1w_defaced.nii', sep=''), 'tmp/')
	anatomical = paste('tmp/', fname, '_T1w_defaced.nii', sep='')
	
	files = c(anatomical=anatomical, functional=functional)

	#realign
	realign_batch = build_spm12_realign(
		filename = functional,
		register_to = 'mean',
		reslice = 'mean'
	)

	realigned = spm12_realign(
		filename = functional,
		register_to = 'mean',
		reslice = 'mean',
		clean = FALSE
	)

	#slicetime
	tr = 3
	nslices = 50
	ta = tr-(tr/nslices)
	n_time_points = 105
	slice_order = c(seq(2, nslices, 2), seq(1, nslices, 2))
	ref_slice = slice_order[median(seq(nslices))]

	st_batch = build_spm12_slice_timing(
		filename = functional,
		time_points = seq(n_time_points),
		nslices = nslices,
		tr = tr,
		ref_slice = ref_slice,
		prefix = 'a'
	)

	st_corrected = spm12_slice_timing(
		filename = realigned[['outfiles']],
		time_points = seq(n_time_points),
		nslices = nslices,
		tr = tr,
		slice_order = slice_order,
		ta = ta,
		ref_slice = ref_slice,
		prefix = 'a',
		clean = FALSE,
		retimg = FALSE
	)

	#coregister
	aimg = st_corrected$outfile
	mean_img = realigned[['mean']]
	check_mean = checknii(mean_img)

	acpc_reorient(
		infiles = c(mean_img, aimg),
		modality = 'T1'
	)

	anatomical = files['anatomical']
	anat_img = checknii(anatomical)

	acpc_reorient(
		infiles = anat_img,
		modality = 'T1'
	)

	coreg = spm12_coregister(
		fixed = mean_img,
		moving = anat_img,
		prefix = 'r'
	)

	coreg_anat = coreg$outfile
	check_coreg = checknii(coreg_anat)

	#segment
	seg_res = spm12_segment(
		filename = coreg_anat,
		affine = 'mni',
		set_origin = FALSE,
		retimg = FALSE,
		clean = FALSE
	)

	#normalize
	bbox = matrix(
		c(-90, -126, -72,
			90, 90, 108),
		nrow = 2, byrow = TRUE
	)

	norm_res = spm12_normalize_write(
		deformation = seg_res$deformation,
		other.files = c(coreg_anat, mean_img, aimg),
		bounding_box = bbox,
		retimg = FALSE
	)

	norm_data = norm_res$outfiles
	names(norm_data) = c('anat', 'mean', 'fmri')

	#smooth
	smooth_res = spm12_smooth(
		filename = norm_data['fmri'],
		fwhm = 8,
		prefix = 's',
		retimg = FALSE,
	)

	final_data = smooth_res$outfiles
	final_fmri = readnii(final_data)
	final_fmri@sform_code <- 4
	final_fmri@qform_code <- 4
	write_nifti(final_fmri, paste('outputs/swar', fname, '_task-music_run-3_bold.nii.gz', sep=''))

	for(tmp in list.files(path='tmp/')){
		file.remove(paste('tmp/', tmp, sep=''))
	}
}

