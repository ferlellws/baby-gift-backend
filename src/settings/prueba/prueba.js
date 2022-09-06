// const { v4: uuidv4 } = require('uuid');

const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();
const ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
const cognito = new AWS.CognitoIdentityServiceProvider({
    apiVersion: "2016-04-18"
});

const TABLE_NAME = process.env.TENANTS_TABLE

AWS.config.update({
    region: "us-east-1",
});


exports.lambdaHandler = async (event) => {
    const tenant = event.queryStringParameters.tenant;
    const environment = event.queryStringParameters.environment;

    const date = new Date();

    const item = {
        tenant: tenant,
        environment: environment,
        date: date.toLocaleDateString()
    }

    const existItem = await existsItem(tenant);

    console.log("USER_POOL_ID: " + process.env.USER_POOL_ID);
    console.log("TENANTS_TABLE: " + process.env.TENANTS_TABLE);
    let body = '';
    if (existItem) {
        body = {
            msg: "El tenant: " + tenant + " ya existe"
        }
    } else {
        const savedItem = await saveItem(item);

        // const userSuperAdmin = {
        //     UserPoolId: process.env.USER_POOL_ID,
        //     Username: 'superadmin',
        //     UserAttributes: [
        //         {
        //             Name: 'email',
        //             Value: 'ferley.leon@tecno.co'
        //         },
        //         {
        //             Name: 'custom:tenant',
        //             Value: tenant
        //         },
        //         {
        //             Name: 'custom:environment',
        //             Value: environment
        //         }
        //     ]
        // }
        // await saveUserCognito(userSuperAdmin);

        const userAdmin = {
            UserPoolId: process.env.USER_POOL_ID,
            Username: 'admin',
            UserAttributes: [
                {
                    Name: 'email',
                    Value: 'ferlellws@gmail.com'
                },
                {
                    Name: 'custom:tenant',
                    Value: tenant
                },
                {
                    Name: 'custom:environment',
                    Value: environment
                }
            ]
        }
        await saveUserCognito(userAdmin);
        body = {...savedItem, ...{msg: "El tenant fue creado exitosamente"}};
    }

    return {
        statusCode: 200,
        body: JSON.stringify(body),
    }

}

async function existsItem(tenant) {
    const params = {
		TableName: TABLE_NAME,
		Key: {
            tenant: {S: tenant}
        }
	};

    return ddb.getItem(params).promise().then((data) => {
        return !!(data.Item);
    }, (err) => {
        console.log("====================");
    });
}

async function saveItem(item) {
    const params = {
		TableName: TABLE_NAME,
		Item: item
	};

    console.log(params)
    
    return dynamo.put(params).promise().then(() => {
        return item;
    });


    // TODO: Crear en people dev-transport-[tenant]
};

async function saveUserCognito(user) {
    const result = await cognito.adminCreateUser(user).promise();
    return result;
}