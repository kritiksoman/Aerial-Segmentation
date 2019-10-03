%% load data
% imds = imageDatastore('train_data.mat','FileExtensions','.mat','ReadFcn',@matReader);
% imds = imageDatastore('3_Ortho_IRRG_train','FileExtensions',{'.tif'},'ReadFcn',@matReader);% for using IR-R-G-D data as input
imds = imageDatastore('3_Ortho_IRRG_train','FileExtensions',{'.tif'});
% imds = imageDatastore('2_Ortho_RGB','FileExtensions',{'.tif'});
classNames = ["ImperviousSurfaces" 
    "Building" 
    "LowVegetation" 
    "Tree" 
    "Car" 
    "Clutter"];
% Define the colormap used dataset.
cmap = [
    255 255 255   % ImperviousSurfaces
    0 0 255       % Building
    0 255 255     % LowVegetation
    0 255 0       % Tree
    255 255 0     % Car
    255 0 0       % Clutter
    ];
cmap = cmap ./ 255;% Normalize between [0 1].

pxds = pixelLabelDatastore('labels_png_train',classNames,1:6);

%% class imbalance
tbl = countEachLabel(pxds);
frequency = tbl.PixelCount/sum(tbl.PixelCount);
bar(1:numel(classNames),frequency);
xticks(1:numel(classNames)); 
xticklabels(tbl.Name);
xtickangle(45);
ylabel('Frequency');

%% train val split
[imdsTrain, imdsVal, pxdsTrain, pxdsVal] = partitionDatastore(imds,pxds);
numTrainingImages = numel(imdsTrain.Files)
numValImages = numel(imdsVal.Files)
% dont keep 7_10 in val??

%% create network
% Specify the network image size. This is typically the same as the traing image sizes.
imageSize = [1000 1000 3];
% imageSize = [300 300 4];

% Specify the number of classes.
numClasses = 6;

% Create DeepLab v3+.
lgraph = deeplabv3plusLayers(imageSize, numClasses, "xception");
% "inceptionresnetv2");
% lgraph = segnetLayers(imageSize, numClasses);

% class weights
imageFreq = tbl.PixelCount ./ tbl.ImagePixelCount;
classWeights = median(imageFreq) ./ imageFreq;
pxLayer = pixelClassificationLayer('Name','labels','Classes',tbl.Name,'ClassWeights',classWeights);
lgraph = replaceLayer(lgraph,"classification",pxLayer);

%% Train options
% pximdsVal = pixelLabelImageDatastore(imdsVal,pxdsVal);% Define validation data.
augmenter = imageDataAugmenter('RandScale',[1 1.3],'RandXReflection',true,'RandYReflection',true);% augment
pximdsVal = randomPatchExtractionDatastore(imdsVal,pxdsVal,[1000,1000],'PatchesPerImage',50,'DataAugmentation',augmenter);% Define validation data.
pximds = randomPatchExtractionDatastore(imdsTrain,pxdsTrain,[1000,1000],'PatchesPerImage',50,'DataAugmentation',augmenter);% Define train data.
% pximds = pixelLabelImageDatastore(imdsTrain,pxdsTrain, 'DataAugmentation',augmenter);% Define train data.
% Define training options. 
options = trainingOptions('sgdm', ...
    'LearnRateSchedule','piecewise',...
    'LearnRateDropPeriod',10,...
    'LearnRateDropFactor',0.3,...
    'Momentum',0.9, ...
    'InitialLearnRate',1e-3, ...
    'L2Regularization',0.005, ...
    'ValidationData',pximdsVal,...
    'MaxEpochs',100, ...  
    'MiniBatchSize',4, ...
    'Shuffle','every-epoch', ...
    'CheckpointPath', 'ckpt', ...
    'VerboseFrequency',2,...
    'Plots','training-progress');
% ,...
%     'ValidationPatience', 4);

%% train 
% pretrainedNetwork='deeplabv3plusResnet18CamVid.mat';data = load(pretrainedNetwork);
% net = data.net;
[net, info] = trainNetwork(pximds,lgraph,options);

%% check result on one image
dataOut = preview(pximdsVal);
idx=1;
I = dataOut.InputImage{idx,1};
GT = dataOut.ResponsePixelLabelImage{idx,1};
C = semanticseg(I, net);
B = labeloverlay(I,C,'Colormap',cmap,'Transparency',0.4);
figure;imshow(B);pixelLabelColorbar(cmap, classNames);title('Predicted');
GT = labeloverlay(I,GT,'Colormap',cmap,'Transparency',0);
figure;imshow(GT);pixelLabelColorbar(cmap, classNames);title('GT');

%% evalaute on test dataset
for i=1:size(cmap,1)
   label(i,1) = {cmap(i,:)*255}; 
end
imdsTest = imageDatastore('test_patch\im','FileExtensions',{'.jpg'});%the folder contains test patches images
pxdsTest = pixelLabelDatastore('test_patch\label',classNames,label);%the folder contains test patches labels
pxdsResults = semanticseg(imdsTest,net, ...
    'MiniBatchSize',4, ...
    'WriteLocation','tmpWrite', ...
    'Verbose',false);
metrics = evaluateSemanticSegmentation(pxdsResults,pxdsTest,'Verbose',false);
metrics.ClassMetrics

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


