# Smart Bike Project

## Project Overview
The Smart Bike project is an innovative solution designed for a marketing company to capture and analyze traffic data in urban environments. It utilizes advanced hardware and software technologies to gather real-time analytics as bikes equipped with the system navigate through town. This data is then processed to provide valuable insights into traffic patterns, which are displayed on a user-friendly dashboard.

## Hardware Components
- **Raspberry Pi**: Serves as the central processing unit.
- **OAK-D Camera**: Attached to the Raspberry Pi, this camera is responsible for capturing real-time video and processing it to detect and analyze traffic.
- **Waveshare 7600X SIM Hat**: Equipped with GPS and 4G LTE functionalities, this module provides internet connectivity through the SIM hat and captures GPS coordinates.

## Software and Technologies
- **AWS (Amazon Web Services)**: Used for storing and processing the traffic analytics sent from the bikes.
- **React**: Powers the frontend dashboard that displays the traffic analytics. The dashboard is designed to be interactive and user-friendly.
- **Firebase**: Hosts the React dashboard.
- **Flask**: Manages the backend operations, including data handling and server-side logic, deployed on AWS Lambda.
- **DynamoDB**: A NoSQL database service provided by AWS for storing the traffic analytics.

## Functionality
1. **Data Capture**: As the bike moves through the town, the OAK-D camera captures video footage which is processed to detect traffic densities and other relevant metrics.
2. **Data Processing**: The Raspberry Pi processes the captured data, extracting valuable traffic analytics.
3. **GPS Integration**: The Waveshare 7600X SIM Hat captures GPS data to geotag the analytics, providing precise location-based insights.
4. **Data Transmission**: Processed data, along with time stamps and GPS coordinates, is transmitted over 4G LTE to AWS.
5. **Dashboard Display**: The collected data is aggregated and displayed on a React-based dashboard, allowing for real-time monitoring and analysis of traffic patterns.

## Deployment
- **Frontend**: The React dashboard is deployed on Firebase, offering a scalable and secure platform for user access.
- **Backend**: The Flask application is deployed on AWS Lambda, ensuring efficient data handling and server-side logic execution.
- **Database**: DynamoDB is used to handle the influx of data, chosen for its scalability and performance in handling large datasets.

## Power Management
The entire system is powered by a robust battery setup, ensuring that the Smart Bike can operate for extended periods without the need for frequent recharging.

## Potential Use Cases
- **Traffic Management**: Assists city planners and traffic management professionals in understanding traffic flow and making informed decisions.
- **Marketing Analysis**: Enables the marketing company to analyze high-traffic areas for potential advertising and promotional activities.
- **Urban Planning**: Provides data-driven insights that can influence future urban development projects.

## Conclusion
Smart Bike is a cutting-edge project that leverages technology to enhance urban mobility analytics. By integrating advanced hardware with sophisticated software solutions, Smart Bike provides key stakeholders with the tools needed to optimize urban environments.
