% matReader reads custom MAT files containing 6 channel multispectral image
% data.
%
%  IMAGE = matReader(FILENAME) returns the first 6 channels of the
%  Multispectral image saved in FILENAME.

% Copyright 2017 The MathWorks, Inc.
function data = matReader(filename)

%     d = load(filename);
%     f = fields(d);
%     data = d.(f{1})(:,:,1:6);

newfilename = strrep(filename,'3_Ortho_IRRG_train','1_DSM');
newfilename = strrep(newfilename,'_IRRG','');
newfilename = strrep(newfilename,'top','dsm');
newfilename = strrep(newfilename,'potsdam_','potsdam_0');
d1=single(imread(filename));
d2=imread(newfilename);
% data=cat(3,d1,d2);
data = cat(3,(d1(:,:,1)-d1(:,:,2))./(d1(:,:,1)+d1(:,:,2)),d1(:,:,3),d2);
end