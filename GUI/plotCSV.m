% Define the filename of the CSV file
filename = 'data_log.csv'; % Replace with your actual file name

% Read the data from the CSV file
data = readtable(filename);

% Assuming the first column is 'Time' and subsequent columns are different variables
% Change these names according to your CSV file headers
time = data.Time;  % Replace with the appropriate column name for the x-axis

% Extract multiple y variables (e.g., Sensor1, Sensor2, Sensor3)
y1 = data.Sensor1; % Replace with your actual column name for the first variable
y2 = data.Sensor2; % Replace with your actual column name for the second variable
y3 = data.Sensor3; % Replace with your actual column name for the third variable

% Create the plot
figure; % Create a new figure window

% Plot the first function
plot(time, y1, '-o', 'LineWidth', 1.5); 
hold on; % Hold on to add more plots

% Plot the second function
plot(time, y2, '-x', 'LineWidth', 1.5);

% Plot the third function
plot(time, y3, '-s', 'LineWidth', 1.5);

% Add grid, labels, and title
grid on; 
xlabel('Time (s)'); % Label for x-axis
ylabel('Sensor Values'); % Label for y-axis
title('Multiple Functions from CSV Data'); % Title of the plot

% Add a legend to differentiate the functions
legend('Sensor 1', 'Sensor 2', 'Sensor 3'); % Adjust according to your variable names

% Release the hold on the current plot
hold off;