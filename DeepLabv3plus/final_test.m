%% final test script
fname = '3_Ortho_IRRG_test\top_potsdam_3_14_IRRG.tif';
A = imread(fname);
h=1000;w=1000;

%% gt
fname = 'labels\top_potsdam_3_14_label.tif';
GT = imread(fname);

%%
idx = 1;
for rIdx=0:h:size(A,1)-h
    for cIdx=0:w:size(A,2)-w
        din(:,:,:,idx) = A(rIdx+1:rIdx+h,cIdx+1:cIdx+w,:);
%         C(:,:,idx) = semanticseg(din(:,:,:,idx), net);
        idx = idx + 1;       
    end
end
%%
C = semanticseg(din, net, 'MiniBatchSize',4);

%% traverse
idx = 1;
for rIdx=0:h:size(A,1)-h
    for cIdx=0:w:size(A,2)-w
        %         imshow(A(rIdx+1:rIdx+h,cIdx+1:cIdx+w));
        %         drawnow();
        %         break;
        B = labeloverlay(A(rIdx+1:rIdx+h,cIdx+1:cIdx+w),C(:,:,idx),'Colormap',cmap,'Transparency',0.4);
        idx = idx + 1;
        dout(rIdx+1:rIdx+h,cIdx+1:cIdx+w,:) = B;
        
    end
    %     break;
end


%% plotting
figure;montage(cat(4,dout,GT));pixelLabelColorbar(cmap, classNames);title(fname);

%% addon functions
function pixelLabelColorbar(cmap, classNames)
% Add a colorbar to the current axis. The colorbar is formatted
% to display the class names with the color.

colormap(gca,cmap)

% Add colorbar to current figure.
c = colorbar('peer', gca);

% Use class names for tick marks.
c.TickLabels = classNames;
numClasses = size(cmap,1);

% Center tick labels.
c.Ticks = 1/(numClasses*2):1/numClasses:1;

% Remove tick mark.
c.TickLength = 0;
end


