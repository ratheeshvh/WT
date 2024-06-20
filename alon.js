const http = require('http');
const url = require('url');
const querystring = require('querystring');
const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);

// Connect to MongoDB
async function connectDB() {
    try {
        await client.connect();
        console.log('Connected to MongoDB');
    } catch (error) {
        console.error('Error connecting to MongoDB:', error);
    }
}

connectDB();

async function onRequest(req, res) {
    const path = url.parse(req.url).pathname;
    console.log('Request for ' + path + ' received');

    const query = url.parse(req.url).query;
    const params = querystring.parse(query);

    const name = params["name"];
    const email = params["email"];
    const phone = params["phone"];
    const address = params["address"];
    const position = params["position"];
    const department = params["department"];
    const qualification = params["qualification"];
    const availability = params["availability"];

    try {
        if (path.includes("/insert")) {
            if (!name || !email || !phone || !address || !position || !department || !qualification || !availability) {
                res.writeHead(400, { 'Content-Type': 'text/plain' });
                res.end('Values not inserted. All fields are required.');
            } else {
                await insertData(req, res, name, email, phone, address, position, department, qualification, availability);
            }
        } else if (path.includes("/delete")) {
            await deleteData(req, res, email);
        } else if (path.includes("/update")) {
            if (!email) {
                res.writeHead(400, { 'Content-Type': 'text/plain' });
                res.end('Email is required for updating.');
            } else {
                await updateData(req, res, email, params);
            }
        } else if (path.includes("/display")) {
            await displayTable(req, res);
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Route not found');
        }
    } catch (error) {
        console.error('Error processing request:', error);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }
}

async function insertData(req, res, name, email, phone, address, position, department, qualification, availability) {
    try {
        const database = client.db('libraryManagement');
        const collection = database.collection('applications');

        const application = { name, email, phone, address, position, department, qualification, availability };
        const result = await collection.insertOne(application);

        console.log(`${result.insertedCount} document inserted`);

        const htmlResponse = `
            <html>
                <head>
                    <title>Application Details</title>
                    <style>
                        table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; }
                        td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; }
                        tr:nth-child(even) { background-color: #dddddd; }
                    </style>
                </head>
                <body>
                    <h1>Application Submitted</h1>
                    <table>
                        <tr><td>Name</td><td>${name}</td></tr>
                        <tr><td>Email</td><td>${email}</td></tr>
                        <tr><td>Phone</td><td>${phone}</td></tr>
                        <tr><td>Address</td><td>${address}</td></tr>
                        <tr><td>Position</td><td>${position}</td></tr>
                        <tr><td>Department</td><td>${department}</td></tr>
                        <tr><td>Qualification</td><td>${qualification}</td></tr>
                        <tr><td>Availability</td><td>${availability}</td></tr>
                    </table>
                </body>
            </html>
        `;
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(htmlResponse);
    } catch (error) {
        console.error('Error inserting data:', error);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }
}

async function deleteData(req, res, email) {
    try {
        const database = client.db('libraryManagement');
        const collection = database.collection('applications');

        const result = await collection.deleteOne({ email });

        if (result.deletedCount === 1) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Application successfully deleted');
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Application not found');
        }
    } catch (error) {
        console.error('Error deleting data:', error);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }
}

async function updateData(req, res, email, params) {
    try {
        const database = client.db('libraryManagement');
        const collection = database.collection('applications');

        const updatedFields = {};
        for (let key in params) {
            if (params.hasOwnProperty(key) && key !== 'email') {
                updatedFields[key] = params[key];
            }
        }

        const result = await collection.updateOne({ email }, { $set: updatedFields });

        if (result.modifiedCount === 1) {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Application successfully updated');
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Application not found');
        }
    } catch (error) {
        console.error('Error updating data:', error);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }
}

async function displayTable(req, res) {
    try {
        const database = client.db('libraryManagement');
        const collection = database.collection('applications');
        const applications = await collection.find({}).toArray();

        let htmlResponse = `
            <html>
                <head>
                    <title>Applications</title>
                    <style>
                        table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; }
                        td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; }
                        tr:nth-child(even) { background-color: #dddddd; }
                    </style>
                </head>
                <body>
                    <h1>Job Applications</h1>
                    <table>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Address</th>
                            <th>Position</th>
                            <th>Department</th>
                            <th>Qualification</th>
                            <th>Availability</th>
                        </tr>
        `;

        applications.forEach(app => {
            htmlResponse += `
                <tr>
                    <td>${app.name}</td>
                    <td>${app.email}</td>
                    <td>${app.phone}</td>
                    <td>${app.address}</td>
                    <td>${app.position}</td>
                    <td>${app.department}</td>
                    <td>${app.qualification}</td>
                    <td>${app.availability}</td>
                </tr>
            `;
        });

        htmlResponse += `
                    </table>
                </body>
            </html>
        `;

        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(htmlResponse);
    } catch (error) {
        console.error('Error displaying data:', error);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
    }
}

http.createServer(onRequest).listen(7050);
console.log('Server has started');
