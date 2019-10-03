%% convert label format
files = dir('labels\*.tif');
fullpaths = fullfile({files.folder}, {files.name});
% classNames = ["ImperviousSurfaces","Building","LowVegetation","Tree","Car","Clutter"];
for i=1:length(fullpaths)
    fname = char(fullpaths(i));
    A = imread(fname);
    label = uint8(A(:,:,1)==255) .* uint8(1*A(:,:,2)==255) .* uint8(A(:,:,3)==255);
    label = label + 2*uint8(A(:,:,1)==0) .* uint8(1*A(:,:,2)==0) .* uint8(A(:,:,3)==255);
    label = label + 3*uint8(A(:,:,1)==0) .* uint8(1*A(:,:,2)==255) .* uint8(A(:,:,3)==255);
    label = label + 4*uint8(A(:,:,1)==0) .* uint8(1*A(:,:,2)==255) .* uint8(A(:,:,3)==0);
    label = label + 5*uint8(A(:,:,1)==255) .* uint8(1*A(:,:,2)==255) .* uint8(A(:,:,3)==0);
    label = label + 6*uint8(A(:,:,1)==255) .* uint8(1*A(:,:,2)==0) .* uint8(A(:,:,3)==0);
    fnamenew = strcat(fname(1:end-4),'.png')
    imwrite(label,fnamenew);
end

% imwrite(label,'tmp/label.png');

%     0, 0, 255;...
%     0, 255, 255;...
%     0, 255, 0;...
%     255, 255, 0;...
%     255, 0, 0];

